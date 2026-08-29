# TRUST-A Framework

TRUST-A is a lightweight engineering framework for reviewing the reliability of AI agents and agentic workflows.

It focuses on six questions that become more important as an AI system gains tools, access, persistence, and autonomy:

- **Truth** — what information should the system trust?
- **Rules** — what must the model never be allowed to redefine?
- **Uncertainty** — how is missing or unreliable evidence represented?
- **Scope** — what can the system actually access or change?
- **Traceability** — can the decision and action be reconstructed?
- **Autonomy** — how much execution authority is justified?

TRUST-A is not a regulatory framework and does not certify that a system is safe. It is a practical design and review method.

## 1. Truth

**Question:** What proves the facts the agent is using?

A model can reason well over incorrect, stale, or ambiguous data. Reliability starts before the prompt.

Make explicit:

- authoritative sources by information type;
- provenance of retrieved or generated data;
- freshness requirements and time semantics;
- conflict resolution between sources;
- allowed fallbacks;
- what happens when the authoritative source is unavailable.

### Good pattern

```text
Customer status → CRM
Current deployment → production runtime
Repository behavior → code + tests
Product decision → accepted specification
```

### Failure mode

The agent searches three sources, finds conflicting values, and silently chooses the most convenient one.

### Practical control

Define a source hierarchy and stop condition.

---

## 2. Rules

**Question:** Which constraints must remain deterministic and non-bypassable?

Prompts are useful instructions. They are usually a poor place to enforce critical invariants on their own.

Keep deterministic where feasible:

- permissions and access controls;
- business invariants;
- financial/risk limits;
- schema validation;
- allowed transitions;
- destructive-action preconditions;
- execution and deployment gates.

### Good pattern

```text
LLM proposes action
      ↓
Deterministic validator
      ↓
Accept / reject
      ↓
Tool execution
```

### Failure mode

A prompt says “never exceed this limit,” but the same model both interprets the situation and decides whether the limit applies.

### Practical control

Move critical rules into code, policy, configuration, or a deterministic validation layer.

---

## 3. Uncertainty

**Question:** What does the system do when it cannot prove something?

Unknown is a valid state. Hiding uncertainty creates false confidence.

Useful explicit states include:

- `UNKNOWN`
- `UNAVAILABLE`
- `STALE`
- `DEGRADED`
- `NOT_OBSERVED`
- `NOT_INVOKED`
- `NOT_APPLICABLE`

The exact vocabulary is less important than preserving the distinction.

### Good pattern

```text
Required data stale
→ mark STALE
→ block action
→ preserve reason
```

### Failure mode

Missing values become `0`, `false`, `healthy`, or “probably fine.”

### Practical control

Define fail-closed behavior for the paths where uncertainty can cause material harm.

---

## 4. Scope

**Question:** What can the agent read, decide, modify, or trigger?

An agent should receive the minimum capability required for its role.

Review:

- read vs write permissions;
- available tools and endpoints;
- repository/database/environment boundaries;
- secrets and credentials;
- destructive capabilities;
- external side effects;
- reversibility of actions.

### Good pattern

A review agent can read code, tests, issues, and CI results but cannot merge or deploy.

### Failure mode

A tool is granted broad write access because it was easier than defining a smaller capability.

### Practical control

Document capabilities explicitly and apply least privilege.

---

## 5. Traceability

**Question:** Can we reconstruct what the system used, decided, and actually did?

Logs that only say “agent completed” are not enough for consequential workflows.

Depending on the system, retain:

- source references and timestamps;
- model / prompt / schema / strategy versions;
- relevant deterministic inputs;
- rules or reason codes triggered;
- tool calls and their outcomes;
- approval events;
- final external actions.

A stage that is explicitly proven `NOT_INVOKED` is not missing trace. A stage whose evidence cannot be established is.

### Good pattern

```text
DECISION
FACTS
RULES TRIGGERED
UNKNOWNS
ACTION
SOURCES
```

### Failure mode

The final action is visible, but nobody can tell which source, version, or rule produced it.

### Practical control

Design the decision trace as a product requirement, not an afterthought.

---

## 6. Autonomy

**Question:** How far should the system act without human approval?

Maximum autonomy is not automatically better.

Use a simple ladder:

1. **READ_ONLY** — inspect and summarize.
2. **RECOMMEND** — propose a decision or action.
3. **ACT_WITH_APPROVAL** — execute after an explicit approval gate.
4. **ACT_AUTONOMOUSLY** — execute within an intentionally bounded scope.

Increase autonomy only when the earlier TRUST-A dimensions support it.

Consider:

- impact of a wrong action;
- reversibility;
- blast radius;
- quality and freshness of evidence;
- strength of deterministic rules;
- observability and rollback;
- confidence in permissions and tool behavior.

### Useful principle

**Reversibility is often a better autonomy signal than raw action size.**

A large but easily reversible internal change may justify more autonomy than a small irreversible external action.

---

# How the dimensions interact

The six dimensions are not independent checkboxes.

Examples:

- weak **Truth** should reduce **Autonomy**;
- stronger **Rules** can make model reasoning safer;
- explicit **Uncertainty** prevents absence from becoming permission;
- narrow **Scope** reduces the consequence of model error;
- good **Traceability** makes failures diagnosable but does not prevent them;
- high **Autonomy** requires stronger controls across the other five dimensions.

A useful architecture is:

```text
Authoritative sources
        ↓
Validation / freshness
        ↓
Context for the agent
        ↓
Agent reasoning
        ↓
Deterministic preconditions
        ↓
Bounded capability
        ↓
Action
        ↓
Decision trace
```

# Review outcomes

Use simple qualitative states:

- **PASS** — explicit and sufficient for the reviewed scope.
- **WARN** — usable, but incomplete or fragile.
- **FAIL** — a gap can plausibly cause a materially wrong or unsafe action.
- **N/A** — genuinely irrelevant to this workflow.

Do not use `N/A` simply because evidence is missing.

# Applying TRUST-A without bureaucracy

TRUST-A should be proportional to consequence.

### Low-impact assistant workflow

A short TRUST-A Lite review may be enough.

### Tool-using internal agent

Document source hierarchy, capability boundaries, failure behavior, and trace.

### Production or externally acting agent

Require deterministic preconditions, explicit permissions, stop conditions, approval policy, observability, and rollback/kill-switch design where relevant.

# Minimum reusable contract

For any important agentic workflow, you should be able to answer:

1. What is the source of truth?
2. Which rules are absolute?
3. When must the system stop rather than guess?
4. What can it actually do?
5. What requires approval?
6. How will we explain the decision later?

If these questions are unclear, increasing model capability or autonomy is usually premature.

## Next

- Run the short review: [TRUST-A Lite](../templates/TRUST-A-LITE.md)
- Define a workflow explicitly: [Agent Contract](../templates/AGENT-CONTRACT.md)
- Automate the review with AI: [TRUST-A Audit Skill](../skills/trust-a-audit/)