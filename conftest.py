import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent


def _has_explicit_week_target(argv):
    """Return True when pytest is being pointed at a specific week folder."""
    for arg in argv[1:]:
        if arg.startswith("-"):
            continue

        candidate = (REPO_ROOT / arg).resolve()
        if candidate.exists():
            rel = candidate.relative_to(REPO_ROOT)
            if rel.parts and rel.parts[0].startswith("week-"):
                return True

        if arg.startswith("week-"):
            return True

    return False


def pytest_sessionstart(session):
    if Path.cwd().resolve() != REPO_ROOT:
        return

    if _has_explicit_week_target(sys.argv):
        return

    pytest.exit(
        "This repository is organized as separate weekly projects. "
        "Run pytest from inside the target week folder instead of the repo root, for example:\n\n"
        "  cd week-3-playwright-polish && pytest\n"
        "  cd week-4-api-testing && pytest\n\n"
        "Root-level pytest collection is intentionally disabled to avoid mixing incompatible configs, browser fixtures, and live API assumptions."
    )
