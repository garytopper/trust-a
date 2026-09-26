# TRUST-A Risk & Autonomy Policy

Use this template to decide how much execution authority a workflow should receive.

Risk and autonomy are orthogonal:

- **autonomy** describes how far the workflow may act without approval;
- **risk** describes the consequence if the action or control fails.

A highly autonomous reversible internal task may be acceptable while a small irreversible external action still requires approval.

## 1. Autonomy ladder

Use the existing TRUST-A autonomy levels:

1. READ_ONLY
2. RECOMMEND
3. ACT_WITH_APPROVAL
4. ACT_AUTONOMOUSLY

Autonomy is a permission decision, not a model capability score.

## 2. Risk classes

Classify the **highest material consequence** of the scoped action.

| Class | Meaning | Typical characteristics | Default control posture |
| --- | --- | --- | --- |
| **R0** | Observation only | read/research, no external mutation | no approval by default; preserve source evidence where material |
| **R1** | Reversible bounded mutation | local/internal change, easy rollback, small blast radius | autonomous execution may be reasonable with deterministic verification |
| **R2** | Shared bounded mutation | affects shared state or collaborators, but rollback/recovery is clear | independent verification for key invariants; approval depends on contract |
| **R3** | Consequential external effect | production, publication, sending, user-affecting action, hard-to-ignore side effect | approval by default unless explicitly pre-authorized by a narrow contract; independent verification expected |
| **R4** | High-consequence / difficult recovery | money, credentials/permissions, security boundary, destructive or difficult-to-reverse action | explicit human approval by default; fail closed on missing evidence; strong independent verification/recovery evidence |

Examples are illustrative. Classify by consequence and recoverability, not by tool name.

## 3. Classification dimensions

Consider:

- impact if wrong;
- reversibility and recovery time;
- blast radius;
- external/user-facing effect;
- financial effect;
- credential, permission, privacy, or security effect;
- strength of deterministic safeguards;
- quality/freshness of evidence;
- observability and rollback.

Model confidence does not lower the risk class.

## 4. Approval policy

Record the decision explicitly:

| Action class | Approval required? | Who/what may approve | Expiry / scope |
| --- | --- | --- | --- |
| R0 |  |  |  |
| R1 |  |  |  |
| R2 |  |  |  |
| R3 |  |  |  |
| R4 |  |  |  |

A prior approval may cover a bounded class of actions only when its scope is explicit. Do not treat a general instruction such as "be autonomous" as permission for unrelated consequential actions.

## 5. Verification policy

| Risk | Minimum expected verification |
| --- | --- |
| R0 | source/provenance checks proportional to the claim |
| R1 | deterministic checks when available; self-check may be sufficient for low-consequence paths |
| R2 | independent verification of key invariants plus recovery path |
| R3 | independent verification and explicit approval unless the narrow contract already authorizes the exact class |
| R4 | strong independent verification, explicit approval, fail-closed behavior, and recovery/rollback evidence where possible |

"Independent" means the verifier is not merely the same executor repeating its own judgment.

## 6. Stop / escalation conditions

Escalate or stop when:

- required evidence is UNKNOWN, NOT_OBSERVED, stale, or contradictory;
- the action exceeds the declared scope;
- the observed risk is higher than the contract's risk class;
- required independent verification fails or cannot run;
- a required approval is missing, expired, ambiguous, or outside scope;
- rollback/recovery required by policy is unavailable.

## 7. Decision rule

A useful mental model is:

~~~text
permitted autonomy
= bounded capability
× consequence
× reversibility
× evidence and verification
~~~

This is not a numeric score. It is a reminder that more capable models do not remove the need for proportionate controls.
