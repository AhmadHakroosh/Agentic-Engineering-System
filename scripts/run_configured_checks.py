#!/usr/bin/env python3
"""Run configured quality commands sequentially and fail on the first error."""

import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("checks", nargs="+", help="keys from delivery.config.json commands")
args = parser.parse_args()
commands = json.loads((ROOT / "delivery.config.json").read_text(encoding="utf-8"))["commands"]

for check in args.checks:
    if check not in commands:
        raise SystemExit(f"Unknown configured check: {check}")
    command = commands[check]
    print(f"Running {check}: {command}", flush=True)
    subprocess.run(command, cwd=ROOT, shell=True, check=True)

