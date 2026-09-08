#!/usr/bin/env python3
"""Sync canonical TRUST-A docs into the self-contained audit Skill."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTICE = (
    "<!-- Generated from {source} by scripts/sync-skill-references.py. "
    "Do not edit manually. -->\n\n"
)

SPECS = (
    (
        "framework/TRUST-A.md",
        "skills/trust-a-audit/references/trust-a-framework.md",
        {
            "(../templates/TRUST-A-LITE.md)": "(trust-a-lite.md)",
            "(../templates/AGENT-CONTRACT.md)": "(agent-contract.md)",
            "(../skills/trust-a-audit/)": "(../SKILL.md)",
        },
    ),
    (
        "templates/TRUST-A-LITE.md",
        "skills/trust-a-audit/references/trust-a-lite.md",
        {
            "(../framework/TRUST-A.md)": "(trust-a-framework.md)",
            "(AGENT-CONTRACT.md)": "(agent-contract.md)",
        },
    ),
    (
        "templates/AGENT-CONTRACT.md",
        "skills/trust-a-audit/references/agent-contract.md",
        {},
    ),
)


def render(source: str, replacements: dict[str, str]) -> str:
    content = (ROOT / source).read_text(encoding="utf-8")
    for old, new in replacements.items():
        content = content.replace(old, new)
    return NOTICE.format(source=source) + content


def sync(check: bool) -> int:
    drifted: list[str] = []

    for source, destination, replacements in SPECS:
        expected = render(source, replacements)
        target = ROOT / destination

        if check:
            actual = target.read_text(encoding="utf-8") if target.exists() else None
            if actual != expected:
                drifted.append(destination)
            continue

        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(expected, encoding="utf-8")
        print(f"synced {source} -> {destination}")

    if drifted:
        print("Skill references are out of sync:", file=sys.stderr)
        for path in drifted:
            print(f"- {path}", file=sys.stderr)
        print("Run: python scripts/sync-skill-references.py", file=sys.stderr)
        return 1

    if check:
        print("Skill references are in sync.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Sync canonical TRUST-A docs into the audit Skill references."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail instead of writing when generated references differ.",
    )
    args = parser.parse_args()
    return sync(check=args.check)


if __name__ == "__main__":
    raise SystemExit(main())
