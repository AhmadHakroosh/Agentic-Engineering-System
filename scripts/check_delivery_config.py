#!/usr/bin/env python3
"""Fail closed when the release contract permits non-deterministic promotion."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "delivery.config.json"
config = json.loads(path.read_text(encoding="utf-8"))

required_commands = {"formatCheck", "lint", "typecheck", "unitTest", "integrationTest", "build", "securityScan"}
missing = sorted(required_commands - set(config.get("commands", {})))
release = config.get("release", {})
errors = []
if config.get("schemaVersion") != "1.0":
    errors.append("schemaVersion must be 1.0")
if missing:
    errors.append(f"missing commands: {', '.join(missing)}")
if release.get("requireImmutableDigest") is not True:
    errors.append("requireImmutableDigest must be true")
if release.get("rebuildOnPromotion") is not False:
    errors.append("rebuildOnPromotion must be false")
if release.get("productionEnvironment") != "production":
    errors.append("productionEnvironment must be production")

if errors:
    print("\n".join(f"ERROR: {error}" for error in errors), file=sys.stderr)
    raise SystemExit(1)
print("Delivery configuration is fail-closed and deterministic")

