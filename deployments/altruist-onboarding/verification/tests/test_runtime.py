"""Runtime boundary tests that do not call a model."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "runtime"))

import agent_runtime  # noqa: E402


def test_question_normalization_collapses_case_and_punctuation():
    assert agent_runtime.normalize_question("Who is my MANAGER?") == "who is my manager"


def test_third_repeated_blocked_question_is_terminal(monkeypatch, tmp_path):
    runtime = agent_runtime.AgentRuntime.__new__(agent_runtime.AgentRuntime)
    runtime.model = "test-model"
    runtime.sessions = {}
    calls = []
    monkeypatch.setattr(runtime, "_ask_model", lambda question: calls.append(question) or "I don't have that.")
    monkeypatch.setattr(agent_runtime, "validate_output", lambda answer: None)
    monkeypatch.setattr(agent_runtime, "prompt_digest", lambda: "test-digest")
    monkeypatch.setattr(agent_runtime, "LOG_PATH", tmp_path / "runtime.jsonl")

    first = runtime.answer("session-1", "Who is my manager?")
    second = runtime.answer("session-1", "who is my manager")
    third = runtime.answer("session-1", "WHO IS MY MANAGER!!!")

    assert len(calls) == 2
    assert third["answer"] == agent_runtime.TERMINAL_REFUSAL
    assert first["answer"] == second["answer"]


def test_output_policy_blocks_internal_leaks():
    with pytest.raises(RuntimeError, match="pre-send policy blocked"):
        agent_runtime.validate_output("See knowledge/factbase.json.")


def test_output_policy_blocks_unattributed_security_assurance():
    with pytest.raises(RuntimeError, match="security assurance"):
        agent_runtime.validate_output("Client data is safe and fully secure.")


def test_output_policy_allows_attributed_public_security_messaging():
    agent_runtime.validate_output(
        "Altruist's public materials describe security messaging; I cannot confirm an assurance."
    )


def test_output_policy_blocks_hazel_attribution_decay():
    """The 2026-07-26 manual run's real bad answer — one attribution, then a run of
    unattributed capability/availability sentences — must be blocked pre-send, not
    just flagged in offline grading."""
    bad = (
        "Hazel is Altruist's AI platform for wealth management. Altruist's public "
        "materials describe it as emerging from the acquisition of Thyme.\n\n"
        "Hazel's capabilities include Ask Hazel, meeting intelligence, a daily digest, "
        "and tax planning.\n\n"
        "It's available to both Altruist-custody firms and independent firms. When "
        "paired with Altruist custody, it can access live account and holdings data. "
        "It connects to CRM, email, calendar, and document systems."
    )
    with pytest.raises(RuntimeError, match="attribution decay"):
        agent_runtime.validate_output(bad)


def test_output_policy_allows_a_properly_reattributed_hazel_answer():
    ok = (
        "Hazel is Altruist's AI platform for wealth management. Altruist's public "
        "materials describe it as emerging from the acquisition of Thyme.\n\n"
        "Altruist's public materials also describe these capabilities: Ask Hazel, "
        "meeting intelligence, a daily digest, and tax planning."
    )
    agent_runtime.validate_output(ok)  # must not raise


def test_ask_model_env_includes_user(monkeypatch, tmp_path):
    """macOS auth is Keychain-backed and resolved via user identity, not just $HOME.
    A stripped subprocess env missing USER produces 'Not logged in' even against a
    correctly authenticated CLAUDE_CONFIG_DIR — confirmed by bisecting the failing
    minimal env directly against the real CLI. USER must always be forwarded."""
    monkeypatch.setenv("USER", "test-user")
    monkeypatch.setenv("ALTRUIST_CLAUDE_CONFIG_DIR", str(tmp_path))
    runtime = agent_runtime.AgentRuntime.__new__(agent_runtime.AgentRuntime)
    runtime.model = "sonnet"
    runtime.config_dir = str(tmp_path)
    runtime.command = "claude"

    captured = {}

    def fake_run(command, **kwargs):
        captured["env"] = kwargs["env"]
        class Result:
            returncode = 0
            stdout = "ok"
            stderr = ""
        return Result()

    monkeypatch.setattr(agent_runtime.subprocess, "run", fake_run)
    runtime._ask_model("hello")
    assert captured["env"].get("USER") == "test-user"
