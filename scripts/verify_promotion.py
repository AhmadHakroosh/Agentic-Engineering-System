#!/usr/bin/env python3
"""Verify immutable promotion metadata before a production job can start."""

import argparse
import re
import sys

SHA = re.compile(r"^[0-9a-f]{40}$")
DIGEST = re.compile(r"^sha256:[0-9a-f]{64}$")

parser = argparse.ArgumentParser()
parser.add_argument("--requested-sha", required=True)
parser.add_argument("--release-sha", required=True)
parser.add_argument("--requested-digest", required=True)
parser.add_argument("--release-digest", required=True)
args = parser.parse_args()

errors = []
if not SHA.fullmatch(args.requested_sha):
    errors.append("requested SHA must be a full lowercase 40-character commit SHA")
if args.requested_sha != args.release_sha:
    errors.append("requested commit does not match the staged release commit")
if not DIGEST.fullmatch(args.requested_digest):
    errors.append("requested digest must be sha256 followed by 64 lowercase hex characters")
if args.requested_digest != args.release_digest:
    errors.append("requested digest does not match the staged artifact digest")
if errors:
    print("\n".join(f"ERROR: {error}" for error in errors), file=sys.stderr)
    sys.exit(1)
print("Promotion metadata matches staged release evidence")

