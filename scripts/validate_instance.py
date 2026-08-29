#!/usr/bin/env python3
"""Validate a delivery JSON instance against the repository's schema subset."""

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse


def load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"ERROR: {path}: {exc}") from exc


def resolve_ref(root: dict, reference: str) -> dict:
    if not reference.startswith("#/"):
        raise ValueError(f"unsupported non-local reference {reference!r}")
    value: object = root
    for part in reference[2:].split("/"):
        part = part.replace("~1", "/").replace("~0", "~")
        if not isinstance(value, dict) or part not in value:
            raise ValueError(f"unresolvable reference {reference!r}")
        value = value[part]
    if not isinstance(value, dict):
        raise ValueError(f"reference {reference!r} does not resolve to a schema")
    return value


def type_matches(expected: str, value: object) -> bool:
    mapping = {
        "object": lambda item: isinstance(item, dict),
        "array": lambda item: isinstance(item, list),
        "string": lambda item: isinstance(item, str),
        "boolean": lambda item: isinstance(item, bool),
        "integer": lambda item: isinstance(item, int) and not isinstance(item, bool),
        "number": lambda item: isinstance(item, (int, float)) and not isinstance(item, bool),
        "null": lambda item: item is None,
    }
    if expected not in mapping:
        raise ValueError(f"unsupported schema type {expected!r}")
    return mapping[expected](value)


def validate(schema: dict, value: object, root: dict, path: str, errors: list[str]) -> None:
    if "$ref" in schema:
        validate(resolve_ref(root, schema["$ref"]), value, root, path, errors)
        return

    if "const" in schema and value != schema["const"]:
        errors.append(f"{path}: expected constant {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: value {value!r} is not one of {schema['enum']!r}")

    expected_type = schema.get("type")
    if expected_type and not type_matches(expected_type, value):
        errors.append(f"{path}: expected {expected_type}, got {type(value).__name__}")
        return

    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            errors.append(f"{path}: string is shorter than {schema['minLength']}")
        if "pattern" in schema and re.search(schema["pattern"], value) is None:
            errors.append(f"{path}: value does not match {schema['pattern']!r}")
        if schema.get("format") == "uri" and not urlparse(value).scheme:
            errors.append(f"{path}: value is not an absolute URI")

    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{path}: array has fewer than {schema['minItems']} items")
        if schema.get("uniqueItems"):
            serialized = [json.dumps(item, sort_keys=True) for item in value]
            if len(serialized) != len(set(serialized)):
                errors.append(f"{path}: array items must be unique")
        item_schema = schema.get("items")
        if item_schema:
            for index, item in enumerate(value):
                validate(item_schema, item, root, f"{path}[{index}]", errors)

    if isinstance(value, dict):
        properties = schema.get("properties", {})
        for required in schema.get("required", []):
            if required not in value:
                errors.append(f"{path}: missing required property {required!r}")
        if schema.get("additionalProperties") is False:
            for key in value.keys() - properties.keys():
                errors.append(f"{path}: unexpected property {key!r}")
        for key, child_schema in properties.items():
            if key in value:
                validate(child_schema, value[key], root, f"{path}.{key}", errors)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("schema", type=Path)
    parser.add_argument("instance", type=Path)
    args = parser.parse_args()

    schema = load_json(args.schema)
    instance = load_json(args.instance)
    if not isinstance(schema, dict):
        raise SystemExit("ERROR: schema root must be an object")

    errors: list[str] = []
    try:
        validate(schema, instance, schema, "$", errors)
    except ValueError as exc:
        raise SystemExit(f"ERROR: {exc}") from exc
    if errors:
        print("\n".join(f"ERROR: {error}" for error in errors), file=sys.stderr)
        raise SystemExit(1)
    print(f"Validated {args.instance} against {args.schema}")


if __name__ == "__main__":
    main()

