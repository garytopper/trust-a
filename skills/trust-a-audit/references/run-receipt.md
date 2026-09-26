<!-- Generated from templates/RUN-RECEIPT.md by scripts/sync-skill-references.py. Do not edit manually. -->

# TRUST-A Run Receipt

Use this template after a meaningful agentic execution to preserve enough evidence for review without creating a full event log.

Do not emit a receipt for trivial Q&A or tiny transformations unless the surrounding workflow requires one.

## Core identity

**Run ID:**

**Agent / workflow ID:**

**Runtime / model:** optional when immaterial

**Completed at:**

**Scoped objective:**

**Contract / policy version:** optional

## Authority

**Autonomy:** READ_ONLY / RECOMMEND / ACT_WITH_APPROVAL / ACT_AUTONOMOUSLY

**Risk:** R0 / R1 / R2 / R3 / R4

**Approval required:** yes / no

**Approval state:** NOT_REQUIRED / PENDING / APPROVED / REJECTED / NOT_OBSERVED

## Outcome

**Outcome:** PASS / WARN / FAIL / ABORTED / AWAITING_APPROVAL

### Summary

What was accomplished or why the run stopped?

### Material actions / changes

- 

## Verification

**Required:** yes / no

**Verification class:** SELF / INDEPENDENT / MIXED / NOT_REQUIRED / NOT_OBSERVED

| Check | Result | Evidence |
| --- | --- | --- |
|  | PASS / WARN / FAIL / NOT_RUN |  |

Do not describe the executor re-reading its own output as independent verification.

## Unknowns / exceptions

Use explicit states rather than permissive defaults.

- UNKNOWN:
- NOT_OBSERVED:
- exception / deviation:

## Evidence and provenance

Prefer references to canonical evidence rather than copied prompts, secrets, private payloads, or full logs.

- source / issue / specification:
- change / commit / pull request:
- test / CI / runtime check:
- approval event:
- other:

## Human-facing handoff

### What I've done

-

### How to test / verify

-

---

For machine-readable receipts, use [schemas/run-receipt.schema.json](run-receipt.schema.json).
