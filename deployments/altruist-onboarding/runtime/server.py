"""Minimal authenticated HTTP adapter for the controlled agent runtime."""

from __future__ import annotations

import hmac
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

try:
    from .agent_runtime import AgentRuntime
except ImportError:
    from agent_runtime import AgentRuntime


class Handler(BaseHTTPRequestHandler):
    runtime: AgentRuntime
    token: str

    def _send(self, status: int, payload: dict[str, str]) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/answer":
            self._send(404, {"error": "not found"})
            return
        # compare_digest, not ==: a plain comparison short-circuits on the first differing
        # byte and leaks the token prefix through response timing.
        presented = self.headers.get("Authorization") or ""
        if not hmac.compare_digest(presented, f"Bearer {self.token}"):
            self._send(401, {"error": "unauthorized"})
            return
        try:
            length = int(self.headers["Content-Length"])
            payload = json.loads(self.rfile.read(length))
            result = self.runtime.answer(payload["session_id"], payload["question"])
        except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
            self._send(400, {"error": str(exc)})
            return
        except RuntimeError as exc:
            self._send(503, {"error": str(exc)})
            return
        self._send(200, result)

    def log_message(self, format: str, *args: object) -> None:
        return


def main() -> None:
    token = os.environ.get("ALTRUIST_RUNTIME_TOKEN")
    model = os.environ.get("ALTRUIST_MODEL")
    owner = os.environ.get("ALTRUIST_CORRECTION_OWNER")
    backup = os.environ.get("ALTRUIST_CORRECTION_BACKUP")
    config_dir = os.environ.get("ALTRUIST_CLAUDE_CONFIG_DIR")
    # OWNER and BACKUP are never read after this check. That is deliberate: the
    # correction loop is a human dependency the builder cannot satisfy (R-02), so it is
    # made to block startup rather than be quietly skipped. See feedback/corrections.md.
    missing = [
        name
        for name, value in (
            ("ALTRUIST_RUNTIME_TOKEN", token),
            ("ALTRUIST_MODEL", model),
            ("ALTRUIST_CORRECTION_OWNER", owner),
            ("ALTRUIST_CORRECTION_BACKUP", backup),
            ("ALTRUIST_CLAUDE_CONFIG_DIR", config_dir),
        )
        if not value
    ]
    if missing:
        raise SystemExit("missing required configuration: " + ", ".join(missing))
    Handler.runtime = AgentRuntime(model=model)
    Handler.token = token
    host = os.environ.get("ALTRUIST_RUNTIME_HOST", "127.0.0.1")
    port = int(os.environ.get("ALTRUIST_RUNTIME_PORT", "8080"))
    server = ThreadingHTTPServer((host, port), Handler)
    print(f"altruist-onboarding runtime listening on http://{host}:{port}/answer "
          f"(model={model})", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
