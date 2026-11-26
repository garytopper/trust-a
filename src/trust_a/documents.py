"""Load strict JSON and validate against the schemas shipped in the wheel."""

import json
from functools import cache
from importlib.resources import files
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

Document = dict[str, Any]
SCHEMAS = {
    "contract": "agent-contract",
    "policy": "risk-policy",
    "receipt": "run-receipt",
    "observations": "observations",
}


def unique_keys(pairs: list[tuple[str, Any]]) -> Document:
    result: Document = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key {key!r}")
        result[key] = value
    return result


def reject_constant(value: str) -> None:
    raise ValueError(f"invalid JSON constant {value}")


def load(path: Path) -> Document:
    try:
        value = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=unique_keys,
            parse_constant=reject_constant,
        )
    except (OSError, ValueError, RecursionError) as exc:
        raise ValueError(f"{path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return value


@cache
def validator(kind: str) -> Draft202012Validator:
    path = files("trust_a.schemas").joinpath(f"{SCHEMAS[kind]}.schema.json")
    schema = json.loads(path.read_text(encoding="utf-8"))
    return Draft202012Validator(schema, format_checker=FormatChecker(["date-time", "uri"]))


class InvalidDocument(ValueError):
    def __init__(self, kind: str, errors: list[str]):
        super().__init__(f"{kind}: " + " | ".join(errors))
        self.kind = kind
        self.errors = errors


def validate(kind: str, value: Document) -> None:
    errors = sorted(f"{e.json_path}: {e.message}" for e in validator(kind).iter_errors(value))
    if errors:
        raise InvalidDocument(kind, errors)
