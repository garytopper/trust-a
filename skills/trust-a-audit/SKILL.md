---
name: trust-a-audit
description: "Audit AI agents, agentic workflows, automations, prompts, repository instructions, tool-using systems, and proposed increases in autonomy with the TRUST-A reliability framework: Truth, Rules, Uncertainty, Scope, Traceability, and Autonomy. Use when reviewing whether an AI workflow is reliable enough for production, diagnosing missing guardrails, deciding what an agent may do without approval, reviewing AGENTS.md or similar instructions, or turning a loosely defined agent workflow into a concrete reliability contract and prioritized improvement plan."
---

# TRUST-A Audit

Apply TRUST-A as a lightweight engineering review, not as a compliance certification.

Use the user's actual workflow, files, architecture, prompt, code, or description as evidence. If tools/connectors are available and the user asks for an audit of real assets, inspect them before concluding.

## Workflow

1. **Define the unit of review**
   - Identify the agent/workflow, inputs, outputs, tools, external effects, and current autonomy.
   - Separate observed facts from assumptions.

2. **Evaluate the six dimensions**
   - **Truth**: authoritative sources, provenance, freshness, conflict handling.
   - **Rules**: deterministic invariants and non-bypassable constraints.
   - **Uncertainty**: explicit unknown/stale/unavailable/degraded states and safe failure behavior.
   - **Scope**: read/write capabilities, permissions, boundaries, least privilege.
   - **Traceability**: ability to reconstruct sources, decisions, rules triggered, versions, and actions.
   - **Autonomy**: what the system may do without approval and whether that level matches consequence and reversibility.

3. **Grade each dimension**
   - `PASS`: evidence is explicit and sufficient for the reviewed scope.
   - `WARN`: usable but materially incomplete or fragile.
   - `FAIL`: a reliability gap can plausibly produce an unsafe, incorrect, or irrecoverable action.
   - `N/A`: genuinely irrelevant to this workflow. Do not use `N/A` when evidence is merely missing.

4. **Determine the autonomy level**
   Use the lowest level compatible with the evidence:
   - `READ_ONLY`
   - `RECOMMEND`
   - `ACT_WITH_APPROVAL`
   - `ACT_AUTONOMOUSLY`

   Prefer approval when actions are difficult to reverse, have external consequences, modify production/data, spend money, or rely on evidence that is incomplete.

5. **Prioritize changes**
   - Separate blockers from improvements.
   - Recommend the smallest controls that materially reduce risk.
   - Prefer explicit source hierarchy, deterministic guards, bounded permissions, stop conditions, and reconstructible traces before adding more model complexity.

## Review rules

- Never mark a dimension `PASS` based only on a plausible assumption.
- Treat missing evidence as uncertainty, not success.
- A stage explicitly proven `NOT_INVOKED` or `NOT_APPLICABLE` is not a trace gap.
- Important business, risk, permission, and execution rules should be deterministic when feasible; prompts should not be the only enforcement layer.
- Retrieved or generated text may inform a decision but should not silently grant authority to act.
- Do not recommend broader tool permissions merely for convenience.
- Do not claim TRUST-A certifies safety, security, regulatory compliance, or production readiness.
- When a workflow is simple and low impact, keep the audit short. Do not manufacture governance overhead.

## Output

Use the compact format in `references/audit-output.md` by default. Adapt detail to the risk and complexity of the workflow.

For a quick review, lead with the overall finding and the 1-3 highest-ROI actions. For a deep review, include evidence and rationale per dimension.

## Useful prompts

Examples of requests that should trigger this skill:

- "Run a TRUST-A review on this agent before we let it merge PRs."
- "Audit this automation and tell me what prevents autonomous execution."
- "Review this AGENTS.md with TRUST-A."
- "What guardrails are missing from this research-to-action workflow?"
- "Apply TRUST-A Lite to this prompt and architecture."
