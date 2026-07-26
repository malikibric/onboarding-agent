"""agentcheck — build-time verification for the Altruist onboarding agent.

Validates the agent's declared knowledge, boundaries, and eval coverage before release.
Stdlib only, by design: release gating must never depend on a third-party install.

    python3 -m agentcheck                 # check the deployment this package lives in
    python3 -m agentcheck --root PATH     # check a specific deployment
    python3 -m agentcheck --json          # machine-readable

Exit 0 = clear. Exit 1 = blocked.
"""

from .loaders import ArtifactError, Deployment, load
from .model import Finding, Report, Severity
from .checks import run_all

__all__ = [
    "ArtifactError",
    "Deployment",
    "Finding",
    "Report",
    "Severity",
    "load",
    "run_all",
]
