"""Decision checks for named host capabilities. An empty finding list allows dispatch."""

from collections.abc import Callable, Mapping
from dataclasses import asdict, dataclass
from hashlib import file_digest, sha256
import json
from pathlib import Path
import re

from .documents import Document, unique_keys, validate


@dataclass(frozen=True)
class Finding:
    code: str
    status: str
    evidence: str
    recommendation: str


def report(stage: str, findings: list[Finding], **details: object) -> Document:
    states = {item.status for item in findings}
    status = "FAIL" if "FAIL" in states else "UNKNOWN" if "UNKNOWN" in states else "PASS"
    return {
        "stage": stage,
        "status": status,
        "findings": [asdict(f) for f in findings],
        **details,
    }


def evidence(ref: str | None, directory: Path, origin: str) -> list[Finding]:
    """Resolve only local content-addressed blobs; never follow a URI to the network."""
    if not ref or not re.fullmatch(r"urn:sha256:[0-9a-f]{64}", ref):
        return [
            Finding(
                "evidence.unobserved",
                "UNKNOWN",
                f"{origin}: {ref}",
                "Supply a local SHA-256 evidence reference and its blob.",
            )
        ]
    digest = ref.removeprefix("urn:sha256:")
    path = directory / digest
    if path.is_symlink() or not path.is_file():
        return [
            Finding(
                "evidence.unavailable",
                "UNKNOWN",
                f"{origin}: {ref}",
                "Supply the referenced regular file in the evidence directory.",
            )
        ]
    try:
        with path.open("rb") as stream:
            actual = file_digest(stream, "sha256").hexdigest()
    except OSError:
        return [
            Finding(
                "evidence.unreadable",
                "UNKNOWN",
                f"{origin}: {ref}",
                "Make the blob readable.",
            )
        ]
    if actual != digest:
        return [
            Finding(
                "evidence.digest",
                "FAIL",
                f"{origin}: {ref}, observed {actual}",
                "Restore the original bytes or correct the observation.",
            )
        ]
    return []


def required_approval(contract: Document, action: Document, rule: Document) -> bool:
    return bool(
        rule["approval_required"]
        or (contract["autonomy"] == "ACT_WITH_APPROVAL" and action["effect"] == "WRITE")
    )


def approval_proof(observed: Document, policy: Document, directory: Path) -> list[Finding]:
    ref = observed["approval"].get("evidence_ref")
    failures = evidence(ref, directory, "approval")
    if failures:
        return failures
    digest = ref.removeprefix("urn:sha256:")
    try:
        data = (directory / digest).read_bytes()
        if sha256(data).hexdigest() != digest:
            raise ValueError("approval evidence changed")
        event = json.loads(data, object_pairs_hook=unique_keys)
        if not isinstance(event, dict):
            raise ValueError("expected an approval event object")
    except (OSError, ValueError, RecursionError) as exc:
        return [
            Finding(
                "approval.event",
                "FAIL",
                str(exc),
                "Supply a structured host approval event.",
            )
        ]
    for key in ("agent_id", "contract_version", "policy_version", "run_id", "action"):
        if event.get(key) != observed[key]:
            return [
                Finding(
                    "approval.scope",
                    "FAIL",
                    f"{ref}: {key} mismatch",
                    "Obtain approval for this exact invocation.",
                )
            ]
    if event.get("decision") != "APPROVED" or event.get("approver") not in policy["approval_authorities"]:
        return [
            Finding(
                "approval.authority",
                "FAIL",
                ref,
                "Collect an affirmative decision from a policy authority.",
            )
        ]
    return []


def preconditions(
    contract: Document,
    policy: Document,
    run_id: str,
    action_id: str,
    observed: Document,
    directory: Path,
    *,
    after_action: bool = False,
) -> list[Finding]:
    for kind, document in [
        ("contract", contract),
        ("policy", policy),
        ("observations", observed),
    ]:
        validate(kind, document)
    findings: list[Finding] = []
    if not after_action and "execution" in observed:
        findings.append(
            Finding(
                "execution.recorded",
                "FAIL",
                observed["execution"]["status"],
                "Supply fresh pre-action observations for a new invocation.",
            )
        )
    for key, expected, actual in [
        ("policy_version", contract["policy_version"], policy["policy_version"]),
        ("agent_id", contract["agent_id"], observed["agent_id"]),
        (
            "contract_version",
            contract["contract_version"],
            observed["contract_version"],
        ),
        (
            "observation.policy_version",
            contract["policy_version"],
            observed["policy_version"],
        ),
        ("run_id", run_id, observed["run_id"]),
        ("action", action_id, observed["action"]),
    ]:
        if expected != actual:
            findings.append(
                Finding(
                    "identity." + key,
                    "FAIL",
                    f"expected {expected}, got {actual}",
                    "Load the records for this exact invocation and policy.",
                )
            )
    action = contract["actions"].get(action_id)
    if action is None:
        return findings + [
            Finding(
                "scope.forbidden",
                "FAIL",
                action_id,
                "Use an explicitly declared capability.",
            )
        ]
    if action["risk"] > contract["risk_ceiling"]:
        findings.append(
            Finding(
                "risk.ceiling",
                "FAIL",
                f"{action['risk']} > {contract['risk_ceiling']}",
                "Escalate the requested action.",
            )
        )
    if action["effect"] == "WRITE" and contract["autonomy"] in (
        "READ_ONLY",
        "RECOMMEND",
    ):
        findings.append(
            Finding(
                "autonomy.write",
                "FAIL",
                contract["autonomy"],
                "Keep this run read-only.",
            )
        )
    if action["effect"] == "WRITE" and action["risk"] == "R0":
        findings.append(
            Finding(
                "risk.mutation",
                "FAIL",
                "WRITE classified R0",
                "Classify the mutation by consequence.",
            )
        )
    for source in action["required_sources"]:
        record = observed["sources"].get(source, {})
        status = record.get("status", "NOT_OBSERVED")
        if status != "VERIFIED":
            findings.append(
                Finding(
                    "truth.source",
                    "UNKNOWN",
                    f"{source}: {status}",
                    "Obtain current, verified input from the configured source.",
                )
            )
        else:
            findings.extend(evidence(record.get("evidence_ref"), directory, source))
    approval = observed["approval"]
    if approval["status"] in ("REJECTED", "PENDING"):
        findings.append(
            Finding(
                "approval.stop",
                "FAIL",
                approval["status"],
                "Resolve the recorded approval gate.",
            )
        )
    elif approval["status"] == "APPROVED":
        findings.extend(approval_proof(observed, policy, directory))
    elif required_approval(contract, action, policy["by_risk"][action["risk"]]):
        findings.append(
            Finding(
                "approval.missing",
                "UNKNOWN",
                approval["status"],
                "Collect an approval scoped to this invocation.",
            )
        )
    return findings


def dispatch(
    contract: Document,
    policy: Document,
    run_id: str,
    action_id: str,
    observed: Document,
    directory: Path,
    handlers: Mapping[str, Callable[[], None]],
) -> Document:
    """Call a host-owned, pre-bound handler only if every precondition passes.

    Adapter errors propagate. A handler that raises may already have produced effects.
    """
    findings = preconditions(contract, policy, run_id, action_id, observed, directory)
    handler = handlers.get(action_id)
    if handler is None:
        findings.append(Finding("scope.unbound", "FAIL", action_id, "Register a bounded host handler."))
    invoked = False
    if not findings and handler is not None:
        handler()
        invoked = True
    return report("dispatch", findings, run_id=run_id, action=action_id, invoked=invoked)
