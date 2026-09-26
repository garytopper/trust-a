<!-- Generated from templates/AGENT-CONTRACT.md by scripts/sync-skill-references.py. Do not edit manually. -->

# Agent Contract

Use this template to make an AI agent or agentic workflow explicit before granting significant tools or autonomy.

The goal is not documentation for its own sake. The contract should answer the questions that would otherwise be rediscovered inside prompts, code, or incidents.

## 1. Purpose

**Workflow / agent:**

**Stable agent / workflow ID:**

**Runtime / model policy:** which runtimes may execute this contract, and what requires re-review?

**Primary outcome:**

**Owner:**

**Current autonomy:** `READ_ONLY` / `RECOMMEND` / `ACT_WITH_APPROVAL` / `ACT_AUTONOMOUSLY`

**Declared risk ceiling:** `R0` / `R1` / `R2` / `R3` / `R4`

**Out of scope:**

---

## 2. Truth · Sources of truth

Define the authoritative source for each information type.

| Information | Authoritative source | Freshness requirement | Allowed fallback | If unavailable |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |
|  |  |  |  |  |

### Source precedence

1.
2.
3.

### Conflict rule

When sources disagree:

```text
...
```

---

## 3. Rules · Hard invariants

List rules that the model cannot override through interpretation.

| Rule | Enforcement layer | Failure outcome |
| --- | --- | --- |
|  | code / policy / config / validation |  |
|  |  |  |

Examples:

- allowed state transitions;
- risk or financial limits;
- required tests/checks;
- schema constraints;
- permissions;
- destructive-action preconditions.

---

## 4. Uncertainty · Stop conditions

The agent must stop, degrade, or request approval when:

- [ ] required evidence is missing;
- [ ] authoritative data is stale;
- [ ] sources conflict beyond the defined resolution rule;
- [ ] a critical validation fails;
- [ ] a required tool/system is unavailable;
- [ ] the requested action is outside scope;
- [ ] other: ...

### Explicit states

Use the states relevant to the workflow, for example:

```text
UNKNOWN
UNAVAILABLE
STALE
DEGRADED
NOT_OBSERVED
NOT_INVOKED
NOT_APPLICABLE
```

Do not replace missing evidence with a permissive default.

---

## 5. Scope · Capabilities and permissions

| Capability | Read / write | External effect | Reversible | Permission / credential | Allowed autonomously |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |
|  |  |  |  |  |  |

### Explicitly forbidden capabilities

- 
- 

---

## 6. Traceability · Decision trace

For consequential decisions, preserve enough evidence to reconstruct:

```text
DECISION
What was decided?

FACTS
Which observed facts mattered?

RULES TRIGGERED
Which deterministic rules or reason codes applied?

UNKNOWNS
What was unavailable, stale, or uncertain?

ACTION
What was actually executed?

SOURCES
Which sources, timestamps, versions, approvals, and tool results support the trace?
```

### Required trace fields

- [ ] source/provenance
- [ ] relevant timestamps
- [ ] model/prompt/schema version where material
- [ ] deterministic rule/reason codes
- [ ] tool/action result
- [ ] approval identity/event where required
- [ ] other: ...

---

## 7. Autonomy · Approval policy

### Current level

`READ_ONLY` / `RECOMMEND` / `ACT_WITH_APPROVAL` / `ACT_AUTONOMOUSLY`

### Autonomous actions

- 

### Actions requiring approval

- 

### Actions that are never allowed

- 

### Required verification

Define the minimum evidence required before a run can be considered complete.

| Risk / action class | Required checks | Independent verification required? | Recovery / rollback evidence |
| --- | --- | --- | --- |
|  |  |  |  |

Self-check and independent verification are different evidence classes. Prefer deterministic checks where they can establish the relevant invariant.

### Run receipt policy

For meaningful executions, record a [Run Receipt](run-receipt.md) containing the stable agent/workflow identity, runtime identity when material, scoped objective, autonomy, risk, verification, approvals, exceptions, outcome, and evidence references.

Do not require receipts for trivial interactions unless the surrounding system needs them.

### Conditions for increasing autonomy

Before promotion, require evidence for:

- [ ] stable source/freshness behavior;
- [ ] deterministic invariants;
- [ ] known failure modes;
- [ ] least-privilege permissions;
- [ ] sufficient decision trace;
- [ ] rollback / recovery where applicable;
- [ ] tests and runtime evidence appropriate to the consequence.

---

## 8. TRUST-A review

| Dimension | Status | Main evidence / gap |
| --- | --- | --- |
| Truth | PASS / WARN / FAIL / N/A |  |
| Rules | PASS / WARN / FAIL / N/A |  |
| Uncertainty | PASS / WARN / FAIL / N/A |  |
| Scope | PASS / WARN / FAIL / N/A |  |
| Traceability | PASS / WARN / FAIL / N/A |  |
| Autonomy | PASS / WARN / FAIL / N/A |  |

### Highest-ROI actions

1.
2.
3.

### Blockers before more autonomy

- 

### Runtime references

- [Risk & Autonomy Policy](risk-autonomy-policy.md)
- [Run Receipt](run-receipt.md)
- [Runtime & Oversight](runtime-oversight.md)

---

This contract should point to canonical code, policies, documentation, or configurations rather than becoming a second source of truth for rules that already exist elsewhere.
