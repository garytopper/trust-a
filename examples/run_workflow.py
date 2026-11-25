"""Run from a consumer project with a copy of the draft fixture and an installed toolkit."""

import argparse
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from trust_a.controls import dispatch
from trust_a.documents import load


def record(directory: Path, event: dict) -> str:
    data = (json.dumps(event, sort_keys=True) + "\n").encode()
    digest = hashlib.sha256(data).hexdigest()
    (directory / digest).write_bytes(data)
    return f"urn:sha256:{digest}"


def write(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Save one synthetic local draft under TRUST-A controls.")
    parser.add_argument("fixture", type=Path)
    parser.add_argument("output", type=Path, help="A new directory for this execution")
    parser.add_argument("--unverified", action="store_true", help="Simulate an unverified catalog")
    args = parser.parse_args()
    args.output.mkdir()
    directory = args.output / "evidence"
    directory.mkdir()
    contract, policy, observed = (
        load(args.fixture / f"{name}.json") for name in ("contract", "policy", "before")
    )
    if args.unverified:
        observed["sources"]["catalog"] = {"status": "UNVERIFIED"}
    manifest = []
    for label, observation in [
        ("catalog", observed["sources"]["catalog"]),
        ("approval", observed["approval"]),
    ]:
        if "evidence_ref" in observation:
            ref = observation["evidence_ref"]
            # These seed files come from the fixed fixture in this example.
            digest = ref.removeprefix("urn:sha256:")
            if len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
                raise ValueError("invalid seed evidence reference")
            shutil.copyfile(args.fixture / "evidence" / digest, directory / digest)
            manifest.append({"label": label, "uri": ref})
    queue: list[str] = []
    decision = dispatch(
        contract,
        policy,
        "sample-1",
        "draft.save",
        observed,
        directory,
        {"draft.save": lambda: queue.append("draft")},
    )
    write(args.output / "decision.json", decision)
    invoked = decision["invoked"]
    execution = "APPLIED" if invoked else "NOT_INVOKED"
    execution_ref = record(
        directory,
        {
            "run_id": "sample-1",
            "queue": queue,
            "status": execution,
            "findings": decision["findings"],
        },
    )
    observed["execution"] = {"status": execution, "evidence_ref": execution_ref}
    manifest.append({"label": "execution", "uri": execution_ref})
    observed["checks"] = []
    checks = []
    outcome = "ABORTED"
    if invoked:
        status = "PASS" if queue == ["draft"] else "FAIL"
        check_ref = record(directory, {"run_id": "sample-1", "expected": ["draft"], "observed": queue})
        manifest.append({"label": "check", "uri": check_ref})
        observed["checks"].append(
            {
                "name": "queue-contents",
                "status": status,
                "class": "SELF",
                "evidence_ref": check_ref,
            }
        )
        checks.append({"name": "queue-contents", "status": status, "evidence_refs": [check_ref]})
        outcome = status
    receipt = {
        "schema_version": "1",
        "agent_id": contract["agent_id"],
        "contract_version": contract["contract_version"],
        "run_id": "sample-1",
        "objective": contract["objective"],
        "completed_at": datetime.now(timezone.utc).isoformat(),
        "risk": contract["actions"]["draft.save"]["risk"],
        "autonomy": contract["autonomy"],
        "material_actions": ["draft.save"] if invoked else [],
        "approval": {
            "required": True,
            "status": "APPROVED",
            "evidence_refs": [observed["approval"]["evidence_ref"]],
        },
        "verification": {
            "required": invoked,
            "class": "SELF" if invoked else "NOT_REQUIRED",
            "checks": checks,
        },
        "outcome": outcome,
        "evidence": manifest,
    }
    write(args.output / "after.json", observed)
    write(args.output / "receipt.json", receipt)
    print(json.dumps({"outcome": outcome, "queue": queue, "decision": decision}))


if __name__ == "__main__":
    main()
