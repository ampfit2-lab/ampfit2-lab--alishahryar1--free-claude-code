"""CLI guard: exec gh pr create only when --repo equals AMP_FIT_EXPECTED_REPO."""

from __future__ import annotations

import os
import sys


def extract_repo(argv: list[str]) -> str | None:
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--repo" and i + 1 < len(argv):
            return argv[i + 1]
        if a.startswith("--repo="):
            return a.split("=", 1)[1]
        i += 1
    return None


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    expected = os.environ.get("AMP_FIT_EXPECTED_REPO") or ""
    repo = extract_repo(args)
    if not expected or not repo or repo != expected:
        return 2
    if not args or args[0] != "pr":
        return 2
    try:
        os.execvp("gh", ["gh", *args])
    except OSError:
        return 2
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
