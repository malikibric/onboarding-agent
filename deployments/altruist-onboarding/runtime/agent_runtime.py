"""Controlled runtime boundary shared by the evaluator and HTTP adapter."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import threading
import time
import unicodedata
import uuid
from dataclasses import dataclass, field
from pathlib import Path

try:
    from .grader import leaks, _fabrications, security_assurances, _attribution_decay
except ImportError:
    from grader import leaks, _fabrications, security_assurances, _attribution_decay

ROOT = Path(__file__).resolve().parents[1]
PROMPT = ROOT / "runtime" / "system-prompt.txt"
BOUNDARIES = ROOT / "knowledge" / "boundaries.json"
LOG_PATH = ROOT / "runtime" / "conversation-log.jsonl"
TIMEOUT = int(os.environ.get("ALTRUIST_RUNTIME_TIMEOUT", "180"))
LOG_RETENTION_DAYS = int(os.environ.get("ALTRUIST_LOG_RETENTION_DAYS", "30"))
RETRY_COUNT = 1
LOG_LOCK = threading.Lock()
TERMINAL_REFUSAL = (
    "I won't have access to that information. Please use an internal source."
)


def prompt_digest() -> str:
    return hashlib.sha256(PROMPT.read_bytes()).hexdigest()


def normalize_question(question: str) -> str:
    normalized = unicodedata.normalize("NFKC", question).casefold()
    normalized = re.sub(r"[^\w\s]", " ", normalized, flags=re.UNICODE)
    return re.sub(r"\s+", " ", normalized).strip()


def _blocked_triggers() -> tuple[str, ...]:
    data = json.loads(BOUNDARIES.read_text(encoding="utf-8"))
    return tuple(
        trigger.casefold()
        for boundary in data["boundaries"]
        if boundary.get("disposition") == "refuse"
        for trigger in boundary.get("triggers", [])
    )


BLOCKED_TRIGGERS = _blocked_triggers()


def is_blocked_question(question: str) -> bool:
    normalized = normalize_question(question)
    return any(trigger in normalized for trigger in BLOCKED_TRIGGERS)


def validate_output(answer: str) -> None:
    reasons = [f"leaks internals: {reason}" for reason in leaks(answer)]
    reasons.extend(_fabrications(answer))
    reasons.extend(security_assurances(answer))
    reasons.extend(_attribution_decay(answer))
    if reasons:
        raise RuntimeError("pre-send policy blocked response: " + "; ".join(reasons))


@dataclass
class Session:
    repeats: dict[str, int] = field(default_factory=dict)


class AgentRuntime:
    def __init__(self, *, model: str | None = None, command: str = "claude") -> None:
        if not PROMPT.exists():
            raise RuntimeError("system prompt is missing; run runtime/build_prompt.py")
        self.model = model or os.environ.get("ALTRUIST_MODEL")
        if not self.model:
            raise RuntimeError("ALTRUIST_MODEL must pin the production model")
        self.config_dir = os.environ.get("ALTRUIST_CLAUDE_CONFIG_DIR")
        if not self.config_dir:
            raise RuntimeError(
                "ALTRUIST_CLAUDE_CONFIG_DIR must point to an isolated Claude config"
            )
        self.command = command
        self.sessions: dict[str, Session] = {}

    def _ask_model(self, question: str) -> str:
        command = [
            self.command,
            "-p",
            "--system-prompt-file",
            str(PROMPT),
            "--allowedTools",
            "",
            "--model",
            self.model,
        ]
        env = {
            "PATH": os.environ.get("PATH", ""),
            "HOME": os.environ.get("HOME", ""),
            "LANG": "C.UTF-8",
            "CLAUDE_CONFIG_DIR": self.config_dir,
            # Login on macOS is backed by the login Keychain, which the CLI resolves
            # using the user identity, not just $HOME — a stripped env missing USER
            # fails with "Not logged in" even with a correctly authenticated
            # CLAUDE_CONFIG_DIR (confirmed by bisecting the minimal env directly: adding
            # USER alone turned the failure into a normal, successful response).
            "USER": os.environ.get("USER", ""),
        }
        for name in ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN"):
            if os.environ.get(name):
                env[name] = os.environ[name]
        last_error = "model returned no response"
        for attempt in range(RETRY_COUNT + 1):
            try:
                proc = subprocess.run(
                    command,
                    input=question,
                    capture_output=True,
                    text=True,
                    timeout=TIMEOUT,
                    check=False,
                    cwd=ROOT,
                    env=env,
                )
            except subprocess.TimeoutExpired:
                last_error = f"model timed out after {TIMEOUT}s"
            else:
                if proc.returncode == 0 and proc.stdout.strip():
                    return proc.stdout.strip()
                last_error = (
                    f"model exited {proc.returncode}: {proc.stderr.strip()[:200]}"
                )
            if attempt < RETRY_COUNT:
                time.sleep(0.2)
        raise RuntimeError(last_error)

    def answer(self, session_id: str, question: str) -> dict[str, str]:
        if not session_id.strip():
            raise ValueError("session_id is required")
        if not question.strip():
            raise ValueError("question is required")
        session = self.sessions.setdefault(session_id, Session())
        normalized = normalize_question(question)
        if is_blocked_question(question):
            session.repeats[normalized] = session.repeats.get(normalized, 0) + 1
            if session.repeats[normalized] >= 3:
                answer = TERMINAL_REFUSAL
            else:
                answer = self._ask_model(question)
        else:
            session.repeats.pop(normalized, None)
            answer = self._ask_model(question)
        validate_output(answer)
        record = {
            "request_id": str(uuid.uuid4()),
            "session_id_hash": hashlib.sha256(session_id.encode()).hexdigest(),
            "question_hash": hashlib.sha256(question.encode()).hexdigest(),
            "answer_hash": hashlib.sha256(answer.encode()).hexdigest(),
            "question_words": str(len(question.split())),
            "answer_words": str(len(answer.split())),
            "model": self.model,
            "prompt_digest": prompt_digest(),
            "timestamp": str(time.time()),
        }
        LOG_PATH.parent.mkdir(exist_ok=True)
        with LOG_LOCK:
            LOG_PATH.touch(mode=0o600, exist_ok=True)
            LOG_PATH.chmod(0o600)
            with LOG_PATH.open("a", encoding="utf-8") as log:
                log.write(json.dumps(record, sort_keys=True) + "\n")
            _prune_log()
        return {"answer": answer, "request_id": record["request_id"]}


def _prune_log() -> None:
    cutoff = time.time() - (LOG_RETENTION_DAYS * 86400)
    if not LOG_PATH.exists():
        return
    kept = []
    for line in LOG_PATH.read_text(encoding="utf-8").splitlines():
        try:
            record = json.loads(line)
            if float(record["timestamp"]) >= cutoff:
                kept.append(line)
        except (json.JSONDecodeError, KeyError, TypeError, ValueError):
            continue
    temporary = LOG_PATH.with_suffix(".tmp")
    temporary.write_text("\n".join(kept) + ("\n" if kept else ""), encoding="utf-8")
    temporary.chmod(0o600)
    temporary.replace(LOG_PATH)
