---
name: trust-a-audit
description: "Audit AI agents, agentic workflows, automations, prompts, repository instructions, tool-using systems, and proposed increases in autonomy with the TRUST-A reliability framework: Truth, Rules, Uncertainty, Scope, Traceability, and Autonomy. Use when reviewing whether an AI workflow is reliable enough for production, diagnosing missing guardrails, deciding what an agent may do without approval, reviewing AGENTS.md or similar instructions, or turning a loosely defined agent workflow into a concrete reliability contract and prioritized improvement plan."
---

# TRUST-A Audit

Apply TRUST-A as a lightweight engineering review, not as a compliance certification.

TRUST-A asks one practical question:

> What must be true before this workflow can be trusted to act?

Treat reliability as a property of the system around the model, not of the model alone:

```text
trusted inputs
+ deterministic guardrails
+ explicit uncertainty
+ bounded capabilities
+ reconstructible decisions
+ proportional autonomy
```

The six dimensions interact. Do not grade them as independent checklist items. In particular:

- weak **Truth** or unresolved **Uncertainty** should constrain **Autonomy**;
- strong deterministic **Rules** can bound probabilistic model reasoning;
- narrow **Scope** reduces the blast radius of model or tool error;
- **Traceability** makes decisions diagnosable but does not make them safe by itself;
- higher **Autonomy** requires stronger evidence and controls across the other dimensions;
- consequence and reversibility matter more than a simplistic notion of action size.

Use the user's actual workflow, files, architecture, prompt, code, or description as evidence. If tools or connectors are available and the user asks for an audit of real assets, inspect them before concluding.

## Load references progressively

Keep the audit proportional, but use the bundled references when they materially improve reliability:

- For a quick, low-impact review, read `references/trust-a-lite.md` and apply its concrete checks.
- For a deep review, consequential workflow, autonomy increase, ambiguous dimension, or disputed finding, read `references/trust-a-framework.md` before grading.
- When the workflow itself is insufficiently specified, or the user needs a remediation artifact, read `references/agent-contract.md` and use it to structure sources of truth, invariants, stop conditions, permissions, approval policy, and decision trace.
- Use `references/audit-output.md` for the default result shape.

Do not require internet access to understand or apply TRUST-A. The bundled references are the runtime knowledge base for this skill.

## Workflow

1. **Define the unit of review**
   - Identify the agent or workflow, intended outcome, inputs, outputs, tools, external effects, current autonomy, and explicit out-of-scope behavior.
   - Separate observed facts, user-provided claims, inferences, and assumptions.
   - Identify what evidence is unavailable before grading.

2. **Evaluate the six dimensions**
   - **Truth**: authoritative sources, provenance, freshness and time semantics, conflict handling, allowed fallbacks, unavailable-source behavior.
   - **Rules**: deterministic invariants, action preconditions, validation layers, and non-bypassable business, risk, permission, schema, or execution constraints.
   - **Uncertainty**: explicit unknown, stale, contradictory, unavailable, degraded, not-observed, not-invoked, and not-applicable states; stop or fail-closed behavior where consequence requires it.
   - **Scope**: read/write capabilities, tools, permissions, credentials, environment boundaries, external effects, reversibility, and least privilege.
   - **Traceability**: ability to reconstruct sources, timestamps, relevant versions, deterministic inputs, rules or reason codes, tool outcomes, approvals, decisions, and actual actions.
   - **Autonomy**: what the system may do without approval and whether that level is justified by consequence, reversibility, blast radius, evidence quality, deterministic controls, observability, and recovery options.

3. **Grade each dimension**
   - `PASS`: evidence is explicit and sufficient for the reviewed scope.
   - `WARN`: usable but materially incomplete or fragile.
   - `FAIL`: a reliability gap can plausibly produce a materially wrong, unsafe, or irrecoverable action.
   - `N/A`: genuinely irrelevant to this workflow. Do not use `N/A` when evidence is merely missing.

4. **Determine the autonomy level**
   Use the lowest level compatible with the evidence:
   - `READ_ONLY`
   - `RECOMMEND`
   - `ACT_WITH_APPROVAL`
   - `ACT_AUTONOMOUSLY`

   Prefer approval when actions are difficult to reverse, have external consequences, modify production or data, spend money, change permissions, affect users, or rely on incomplete evidence.

   Do not recommend `ACT_AUTONOMOUSLY` merely because every dimension has some control. Explain why the combined evidence justifies autonomous execution and name the conditions that would invalidate that recommendation.

5. **Prioritize changes**
   - Separate blockers from improvements.
   - Recommend the smallest controls that materially reduce risk.
   - Prefer explicit source hierarchy, deterministic guards, bounded permissions, stop conditions, approval gates, and reconstructible traces before adding more model complexity.
   - Avoid generic governance work that does not change a plausible failure mode.

## Review rules

- Never mark a dimension `PASS` based only on a plausible assumption.
- Treat missing evidence as uncertainty, not success.
- A stage explicitly proven `NOT_INVOKED` or `NOT_APPLICABLE` is not a trace gap.
- Important business, risk, permission, and execution rules should be deterministic when feasible; prompts should not be the only enforcement layer.
- Retrieved or generated text may inform a decision but should not silently grant authority to act.
- Do not recommend broader tool permissions merely for convenience.
- Do not confuse observability with prevention: good logs do not compensate for missing guards.
- Do not confuse model confidence with evidence quality.
- Do not claim TRUST-A certifies safety, security, regulatory compliance, or production readiness.
- When a workflow is simple and low impact, keep the audit short. Do not manufacture governance overhead.

## Output

Use the compact format in `references/audit-output.md` by default. Adapt detail to the risk and complexity of the workflow.

For a quick review, lead with the overall finding and the 1-3 highest-ROI actions. For a deep review, include evidence, gap, and smallest useful action per dimension.

When recommending an autonomy level, state the main reason for the ceiling. If the recommendation depends on an assumption or missing runtime evidence, make that explicit.

## Useful prompts

Examples of requests that should trigger this skill:

- "Run a TRUST-A review on this agent before we let it merge PRs."
- "Audit this automation and tell me what prevents autonomous execution."
- "Review this AGENTS.md with TRUST-A."
- "What guardrails are missing from this research-to-action workflow?"
- "Apply TRUST-A Lite to this prompt and architecture."
