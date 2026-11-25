"""Console interface with stable exit codes and structured diagnostics."""

import argparse
import json
from importlib.metadata import version
from pathlib import Path

from .audit import audit
from .controls import Finding, preconditions, report
from .demo import demo
from .documents import Document, InvalidDocument, SCHEMAS, load, validate


def human(result: Document) -> str:
    if result["stage"] == "demo":
        rows = ["Scenario          | Declaration queue | Guarded queue | Decision"]
        for case in result["scenarios"]:
            baseline = ", ".join(case["declaration_queue"]) or "empty"
            guarded = ", ".join(case["guarded_queue"]) or "empty"
            reasons = ", ".join(f["code"] for f in case["decision"]["findings"]) or "allowed"
            rows.append(f"{case['scenario']:17} | {baseline:17} | {guarded:13} | {reasons}")
        return "\n".join(rows)
    rows = [f"{result['stage']}: {result['status']}"]
    for key in ("document", "run_id", "outcome", "action"):
        if key in result:
            rows.append(f"  {key}: {result[key]}")
    for item in result["findings"]:
        rows.extend(
            [
                f"  {item['status']} {item['code']} — {item['evidence']}",
                f"    {item['recommendation']}",
            ]
        )
    for ref in result.get("evidence_references", []):
        rows.append(f"  evidence: {ref}")
    return "\n".join(rows)


def main() -> int:
    parser = argparse.ArgumentParser(prog="trust-a", description="Local TRUST-A developer toolkit")
    parser.add_argument("--version", action="version", version=version("trust-a-toolkit"))
    commands = parser.add_subparsers(dest="command", required=True)
    schemas = commands.add_parser("validate", help="Check document syntax against a bundled schema")
    schemas.add_argument("kind", choices=SCHEMAS)
    schemas.add_argument("file", type=Path)
    pre = commands.add_parser("check", help="Evaluate preconditions without invoking a handler")
    audit_cmd = commands.add_parser("audit", help="Compare a receipt with host observations and evidence")
    for command in [pre, audit_cmd]:
        command.add_argument("contract", type=Path)
        command.add_argument("policy", type=Path)
        command.add_argument("--evidence-dir", required=True, type=Path)
    pre.add_argument("observations", type=Path)
    pre.add_argument("--run-id", required=True)
    pre.add_argument("--action", required=True)
    audit_cmd.add_argument("receipt", type=Path)
    audit_cmd.add_argument("--observations", type=Path)
    comparison = commands.add_parser("demo", help="Observe both simulated queues on five fixed proposals")
    for command in [schemas, pre, audit_cmd, comparison]:
        command.add_argument("--json", action="store_true", help="Emit one JSON document")
    args = parser.parse_args()
    try:
        if args.command == "demo":
            result = demo()
        elif args.command == "validate":
            validate(args.kind, load(args.file))
            result = report("schema", [], document=args.kind)
        else:
            contract, policy = load(args.contract), load(args.policy)
            if args.command == "audit":
                observed = load(args.observations) if args.observations else None
                result = audit(contract, policy, load(args.receipt), observed, args.evidence_dir)
            else:
                findings = preconditions(
                    contract,
                    policy,
                    args.run_id,
                    args.action,
                    load(args.observations),
                    args.evidence_dir,
                )
                result = report("preconditions", findings, run_id=args.run_id, action=args.action)
        code = 0 if result.get("status", "PASS") == "PASS" else 1
    except InvalidDocument as exc:
        result = report(
            "input",
            [Finding("schema.invalid", "FAIL", error, "Correct the document.") for error in exc.errors],
            document=exc.kind,
        )
        code = 2
    except ValueError as exc:
        result = report(
            "input",
            [Finding("input.invalid", "FAIL", str(exc), "Supply a readable JSON object.")],
        )
        code = 2
    print(json.dumps(result, indent=2) if args.json else human(result))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
