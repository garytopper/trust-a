<!-- Generated from framework/RUNTIME-OVERSIGHT.md by scripts/sync-skill-references.py. Do not edit manually. -->

# TRUST-A Runtime and Oversight

TRUST-A's six dimensions remain the core review model. Runtime governance is not a seventh dimension; it is the operational layer that turns the six dimensions into observable execution evidence.

The runtime layer answers two questions:

1. **Before execution:** what is this agent or workflow allowed to do, under which conditions?
2. **After execution:** what actually happened, what evidence supports it, and did the run respect the contract?

## Stable agent identity vs runtime identity

Treat the agent or workflow as a stable operational identity that can outlive any one model, provider, prompt version, or tool runtime.

~~~text
agent / workflow identity
        |
        +-- purpose
        +-- responsibilities
        +-- scope
        +-- approval policy
        +-- verification policy
        |
        +-- runtime A today
        +-- runtime B tomorrow
~~~

A runtime change should not silently redefine the agent's permissions or responsibilities.

For material workflows, record:

- a stable agent_id or workflow ID;
- the runtime/model identity used for the run when relevant;
- the contract/policy version when relevant;
- the scoped objective for the run.

## Contract before action

The [Agent Contract](agent-contract.md) describes intended behavior:

- sources of truth;
- deterministic rules;
- stop conditions;
- capabilities;
- autonomy;
- risk class;
- approval gates;
- required verification;
- trace requirements.

The contract should point to canonical implementation sources rather than duplicating them.

## Receipt after action

A [Run Receipt](run-receipt.md) records material execution evidence.

A useful receipt is compact enough to emit routinely but strong enough to answer:

- who or what acted;
- with which runtime;
- toward which scoped objective;
- under which autonomy and risk policy;
- what changed or was triggered;
- what verification ran;
- whether verification was self or independent;
- what approval was required and observed;
- what remained unknown or exceptional;
- what the final outcome was;
- where supporting evidence lives.

A receipt is not a full prompt dump or event log. Prefer references to canonical evidence over copied sensitive payloads.

## Self-check is not independent verification

An executor can and should check its own work, but self-verification and independent verification are different evidence classes.

Examples of independent verification include:

- CI that evaluates a submitted change;
- deterministic invariant or schema checks outside the agent's reasoning;
- a separate reviewer with isolated context;
- a human approval gate;
- an external runtime health check.

The strongest verification mechanism depends on the failure mode. Deterministic checks are often preferable to asking another model whether the first model "looks correct."

## Oversight states

Preserve the difference between absence and evidence.

Useful states include:

- NOT_REQUIRED — policy says the step does not apply;
- NOT_INVOKED — the step was intentionally not run and this is proven;
- NOT_OBSERVED — the system cannot establish whether it happened;
- UNKNOWN — evidence is insufficient to classify the state;
- PENDING — a required gate or verification has not completed.

Do not turn NOT_OBSERVED or UNKNOWN into PASS.

## Oversight metrics

Metrics are optional and only useful when enough runtime evidence exists.

Three useful families are:

- **coverage** — what proportion of material runs/actions produced the required trace or verification;
- **review latency** — how long required review or approval remained unresolved;
- **escalation rate** — how often runs correctly surfaced a condition requiring human or independent review.

These metrics describe the oversight system. They do not certify that an agent is safe.

## Minimal runtime loop

~~~text
Objective
   ↓
Agent Contract
   ↓
Risk + autonomy decision
   ↓
Execution
   ↓
Verification
   ↓
Run Receipt
   ↓
Audit / human attention when required
~~~

The intended direction is simple: increase autonomy only when the surrounding evidence, controls, scope, reversibility, and oversight justify it.

## Related documents

- [TRUST-A Framework](trust-a-framework.md)
- [Agent Contract](agent-contract.md)
- [Risk & Autonomy Policy](risk-autonomy-policy.md)
- [Run Receipt](run-receipt.md)
