# TRUST-A Lite

A five-minute reliability review for AI agents and agentic workflows.

Use this before shipping a new workflow, adding tools, increasing permissions, or moving from recommendation to autonomous execution.

## Review

### T · Truth

- [ ] Authoritative sources are explicit.
- [ ] Provenance is available where it matters.
- [ ] Freshness/time requirements are defined.
- [ ] Conflicting or unavailable sources have a defined outcome.

**Status:** `PASS` / `WARN` / `FAIL` / `N/A`

### R · Rules

- [ ] Critical invariants are explicit.
- [ ] Important business/risk/permission rules are deterministic where feasible.
- [ ] The LLM cannot silently bypass hard constraints.
- [ ] Action preconditions are validated before execution.

**Status:** `PASS` / `WARN` / `FAIL` / `N/A`

### U · Uncertainty

- [ ] Missing, stale, degraded, or contradictory evidence remains explicit.
- [ ] Unknown is not converted into success or permission.
- [ ] Fail-closed behavior exists for consequential paths.
- [ ] `NOT_INVOKED` and `NOT_APPLICABLE` are distinguishable from missing evidence where useful.

**Status:** `PASS` / `WARN` / `FAIL` / `N/A`

### S · Scope

- [ ] Read and write capabilities are explicit.
- [ ] Permissions follow least privilege.
- [ ] External/destructive effects are bounded.
- [ ] The agent cannot access unrelated systems merely for convenience.

**Status:** `PASS` / `WARN` / `FAIL` / `N/A`

### T · Traceability

- [ ] Sources and important versions can be reconstructed.
- [ ] Rules/reason codes that influenced the decision are preserved.
- [ ] Tool calls and actual actions are observable where required.
- [ ] Approval events are recorded for supervised actions.

**Status:** `PASS` / `WARN` / `FAIL` / `N/A`

### A · Autonomy

- [ ] The current autonomy level is explicit.
- [ ] The consequence and reversibility of actions justify that level.
- [ ] Higher-risk actions have approval, rollback, or stop controls as appropriate.
- [ ] Increased autonomy is an explicit decision, not an accidental side effect of new tooling.

**Status:** `PASS` / `WARN` / `FAIL` / `N/A`

## Result

```text
TRUST-A REVIEW

Overall: PASS | WARN | FAIL
Recommended autonomy: READ_ONLY | RECOMMEND | ACT_WITH_APPROVAL | ACT_AUTONOMOUSLY

Truth          ...
Rules          ...
Uncertainty    ...
Scope          ...
Traceability   ...
Autonomy       ...

Key findings
1.
2.
3.

Highest-ROI actions
1.
2.
3.

Blockers before more autonomy
-
```

## Interpretation

- **PASS** — explicit and sufficient for the reviewed scope.
- **WARN** — usable but materially incomplete or fragile.
- **FAIL** — the gap can plausibly cause a materially wrong or unsafe action.
- **N/A** — genuinely irrelevant. Missing evidence is not `N/A`.

Keep the review proportional. If the workflow is low impact, stop here. If it can modify production, data, money, permissions, or external systems, continue with the full [TRUST-A Framework](../framework/TRUST-A.md) and [Agent Contract](AGENT-CONTRACT.md).