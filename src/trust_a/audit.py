"""Reconcile one receipt with the host's observation of a single bounded action."""

from pathlib import Path

from .controls import Finding, approval_proof, evidence, preconditions, report, required_approval
from .documents import Document, validate


def discrepancy(field: str, expected: object, actual: object) -> Finding:
    return Finding(
        "receipt." + field,
        "FAIL",
        f"expected {expected!r}, got {actual!r}",
        "Reconcile the receipt with the contract, policy and host observation.",
    )


def verification_findings(
    verification: Document, rule: Document, observations: Document, directory: Path
) -> list[Finding]:
    findings = []
    claimed = verification["checks"]
    recorded = observations.get("checks", [])
    for checks in [claimed, recorded]:
        names = [item["name"] for item in checks]
        if len(names) != len(set(names)):
            return [
                Finding(
                    "verification.ambiguous",
                    "FAIL",
                    str(names),
                    "Use unique check names.",
                )
            ]
    claimed_by_name = {c["name"]: c for c in claimed}
    observed_by_name = {c["name"]: c for c in recorded}
    for name in sorted(set(claimed_by_name) | set(rule["required_checks"]) | set(observed_by_name)):
        claim, observation = claimed_by_name.get(name), observed_by_name.get(name)
        if claim is None or observation is None:
            findings.append(
                Finding(
                    "verification.missing",
                    "UNKNOWN",
                    name,
                    "Provide both the named receipt check and its host observation.",
                )
            )
            continue
        if claim["status"] != observation["status"]:
            findings.append(discrepancy("verification.status", observation["status"], claim["status"]))
        ref = observation.get("evidence_ref")
        if observation["status"] != "NOT_RUN":
            findings.extend(evidence(ref, directory, name))
            if ref and ref not in claim.get("evidence_refs", []):
                findings.append(discrepancy("verification.reference", ref, claim.get("evidence_refs", [])))
        if name in rule["required_checks"]:
            if observation["status"] != "PASS":
                state = "UNKNOWN" if observation["status"] == "NOT_RUN" else "FAIL"
                findings.append(
                    Finding(
                        "verification.result",
                        state,
                        f"{name}: {observation['status']}",
                        "Complete the required check successfully.",
                    )
                )
            if rule["verification"] == "INDEPENDENT" and observation["class"] != "INDEPENDENT":
                findings.append(
                    Finding(
                        "verification.independence",
                        "FAIL",
                        f"{name}: {observation['class']}",
                        "Use a verifier independent of the executor for this specific check.",
                    )
                )
    classes = {c["class"] for c in recorded if c["status"] != "NOT_RUN"}
    if len(classes) == 2:
        expected = "MIXED"
    elif classes:
        expected = next(iter(classes))
    else:
        expected = "NOT_OBSERVED" if rule["required_checks"] or claimed else "NOT_REQUIRED"
    if expected != verification["class"]:
        findings.append(discrepancy("verification.class", expected, verification["class"]))
    return findings


def audit(
    contract: Document,
    policy: Document,
    receipt: Document,
    observations: Document | None,
    directory: Path,
) -> Document:
    for kind, doc in [("contract", contract), ("policy", policy), ("receipt", receipt)]:
        validate(kind, doc)
    findings = []
    for field in ["agent_id", "contract_version", "autonomy"]:
        if field not in receipt:
            findings.append(
                Finding("receipt.unobserved", "UNKNOWN", field, "Record the applicable contract version.")
            )
        elif receipt[field] != contract[field]:
            findings.append(discrepancy(field, contract[field], receipt.get(field)))
    if policy["policy_version"] != contract["policy_version"]:
        findings.append(discrepancy("policy_version", contract["policy_version"], policy["policy_version"]))
    if receipt["risk"] > contract["risk_ceiling"]:
        findings.append(
            Finding(
                "risk.ceiling",
                "FAIL",
                receipt["risk"],
                "Investigate the reported consequence.",
            )
        )
    actions = receipt.get("material_actions")
    if actions is None:
        findings.append(
            Finding(
                "actions.unobserved",
                "UNKNOWN",
                "material_actions omitted",
                "Explicitly record the actions or an observed empty list.",
            )
        )
    for action in actions or []:
        if action not in contract["actions"]:
            findings.append(
                Finding(
                    "scope.forbidden",
                    "FAIL",
                    action,
                    "Investigate the out-of-scope action.",
                )
            )
    for field in ["unknowns", "exceptions"]:
        if receipt.get(field):
            findings.append(
                Finding(
                    "receipt." + field,
                    "UNKNOWN",
                    str(receipt[field]),
                    "Resolve or review the disclosed uncertainty or exception.",
                )
            )
    manifest = {item["uri"] for item in receipt["evidence"]}
    for uri in sorted(manifest):
        findings.extend(evidence(uri, directory, "receipt.evidence"))
    linked = set(receipt["approval"].get("evidence_refs", []))
    for check in receipt["verification"]["checks"]:
        linked.update(check.get("evidence_refs", []))
    if observations is None:
        findings.append(
            Finding(
                "observations.missing",
                "UNKNOWN",
                receipt["run_id"],
                "Supply observations collected by the host adapter.",
            )
        )
    else:
        validate("observations", observations)
        action_id = observations["action"]
        execution = observations.get("execution", {})
        state = execution.get("status", "NOT_OBSERVED")
        if state == "NOT_OBSERVED":
            findings.append(
                Finding(
                    "execution.unknown",
                    "UNKNOWN",
                    state,
                    "Collect an execution observation.",
                )
            )
        else:
            findings.extend(evidence(execution.get("evidence_ref"), directory, "execution"))
            if execution.get("evidence_ref"):
                linked.add(execution["evidence_ref"])
            expected_actions = [action_id] if state == "APPLIED" else []
            if actions is not None and actions != expected_actions:
                findings.append(discrepancy("material_actions", expected_actions, actions))
        checks = preconditions(
            contract, policy, receipt["run_id"], action_id, observations, directory, after_action=True
        )
        # A proven stop may be compliant even when preconditions did not permit dispatch.
        findings.extend(f for f in checks if state != "NOT_INVOKED" or f.code.startswith("identity."))
        approval = receipt["approval"]
        host_approval = observations["approval"]
        if approval["status"] != host_approval["status"]:
            findings.append(discrepancy("approval.status", host_approval["status"], approval["status"]))
        if host_approval["status"] == "APPROVED":
            if state == "NOT_INVOKED":
                findings.extend(approval_proof(observations, policy, directory))
            ref = host_approval.get("evidence_ref")
            if ref and ref not in approval.get("evidence_refs", []):
                findings.append(discrepancy("approval.reference", ref, approval.get("evidence_refs", [])))
        action_spec = contract["actions"].get(action_id)
        # Verification of the effect is due only after invocation. Still reconcile
        # any checks claimed on a stopped run against their host observations.
        verification_rule = {"verification": "NOT_REQUIRED", "required_checks": []}
        if action_spec:
            rule = policy["by_risk"][action_spec["risk"]]
            if receipt["risk"] != action_spec["risk"]:
                findings.append(discrepancy("risk", action_spec["risk"], receipt["risk"]))
            needed = required_approval(contract, action_spec, rule)
            if approval["required"] != needed:
                findings.append(discrepancy("approval.required", needed, approval["required"]))
            if state == "APPLIED":
                verification_rule = rule
                for source in action_spec["required_sources"]:
                    ref = observations["sources"].get(source, {}).get("evidence_ref")
                    if ref:
                        linked.add(ref)
        if state != "NOT_OBSERVED":
            needed = bool(verification_rule["required_checks"])
            if receipt["verification"]["required"] != needed:
                findings.append(
                    discrepancy("verification.required", needed, receipt["verification"]["required"])
                )
            findings.extend(
                verification_findings(receipt["verification"], verification_rule, observations, directory)
            )
        if state == "APPLIED" and receipt["outcome"] == "AWAITING_APPROVAL":
            findings.append(discrepancy("outcome", "action already applied", "AWAITING_APPROVAL"))
        if state == "NOT_INVOKED" and receipt["outcome"] == "PASS":
            findings.append(discrepancy("outcome", "stopped before the scoped action", "PASS"))
    for missing in sorted(linked - manifest):
        findings.append(
            Finding(
                "evidence.unlisted",
                "UNKNOWN",
                missing,
                "Include the supporting reference in the receipt evidence list.",
            )
        )
    return report(
        "audit",
        findings,
        run_id=receipt["run_id"],
        outcome=receipt["outcome"],
        evidence_references=sorted(manifest),
    )
