#!/usr/bin/env python3
"""Require populated delivery metadata and completed author attestations."""

import argparse
import re
import sys
from pathlib import Path

FIELDS = (
    "Reference",
    "Requirements contract",
    "Design contract",
    "Delivery packet",
    "Summary",
    "Explicitly out of scope",
    "Acceptance criteria",
    "Checks run",
    "Independent review",
    "Residual risks",
    "Rollout",
    "Rollback",
    "Observability",
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("body_file", type=Path)
    args = parser.parse_args()
    body = args.body_file.read_text(encoding="utf-8")

    errors = []
    for field in FIELDS:
        match = re.search(rf"^- {re.escape(field)}:\s*(\S.*)$", body, re.MULTILINE)
        if not match:
            errors.append(f"populate '- {field}:'")

    unchecked = re.findall(r"^- \[ \] (.+)$", body, re.MULTILINE)
    if unchecked:
        errors.append("complete all author attestations")
    if not re.search(r"^- \[[xX]\] ", body, re.MULTILINE):
        errors.append("author attestations are missing")

    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors), file=sys.stderr)
        raise SystemExit(1)
    print("Pull request delivery metadata is populated")


if __name__ == "__main__":
    main()

