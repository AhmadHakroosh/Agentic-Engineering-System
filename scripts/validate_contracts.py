#!/usr/bin/env python3
"""Validate contract files structurally without third-party dependencies."""

import json
import sys
from pathlib import Path

from validate_instance import validate as validate_instance

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "contracts" / "schemas"
EXAMPLES = ROOT / "contracts" / "examples"


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def load(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"{path.relative_to(ROOT)}: {exc}")
    if not isinstance(data, dict):
        fail(f"{path.relative_to(ROOT)} must contain a JSON object")
    return data


def main() -> None:
    schema_files = sorted(SCHEMAS.glob("*.schema.json"))
    if not schema_files:
        fail("no schemas found")
    ids: set[str] = set()
    for path in schema_files:
        schema = load(path)
        for key in ("$schema", "$id", "title", "type"):
            if key not in schema:
                fail(f"{path.relative_to(ROOT)} missing {key}")
        if schema["$id"] in ids:
            fail(f"duplicate schema id: {schema['$id']}")
        ids.add(schema["$id"])
        if schema["type"] != "object" or schema.get("additionalProperties") is not False:
            fail(f"{path.relative_to(ROOT)} must be a closed object schema")

    for path in sorted(EXAMPLES.glob("*.json")):
        example = load(path)
        if example.get("schemaVersion") != "1.0":
            fail(f"{path.relative_to(ROOT)} has unsupported schemaVersion")
        contract_name = path.name.removesuffix(".example.json")
        schema_path = SCHEMAS / f"{contract_name}.schema.json"
        if not schema_path.exists():
            fail(f"{path.relative_to(ROOT)} has no matching schema")
        errors: list[str] = []
        validate_instance(load(schema_path), example, load(schema_path), "$", errors)
        if errors:
            fail(f"{path.relative_to(ROOT)}: {'; '.join(errors)}")

    print(f"Validated {len(schema_files)} schemas and {len(list(EXAMPLES.glob('*.json')))} examples")


if __name__ == "__main__":
    main()
