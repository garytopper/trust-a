# TRUST-A

**A practical reliability framework for AI agents and agentic workflows.**

TRUST-A helps teams answer a simple question before giving an AI system more responsibility:

> **What must be true before we can trust this workflow to act?**

It is intentionally lightweight. TRUST-A is not a compliance standard, certification, or security product. It is an engineering review framework for making sources, hard rules, uncertainty, permissions, evidence, and autonomy explicit.

## The framework

| Dimension | Question |
| --- | --- |
| **T · Truth** | What information is authoritative, fresh, and traceable to a source? |
| **R · Rules** | Which constraints must remain deterministic and non-bypassable? |
| **U · Uncertainty** | What happens when data is missing, stale, contradictory, or unavailable? |
| **S · Scope** | What may the agent read, decide, modify, or trigger? |
| **T · Traceability** | Can we reconstruct what the system used, decided, and actually did? |
| **A · Autonomy** | How far may it act without human approval? |

The core principle is simple:

```text
Reliable agentic workflow
= trusted inputs
+ deterministic guardrails
+ explicit uncertainty
+ bounded capabilities
+ reconstructible decisions
+ proportional autonomy
```

## Start in five minutes

Use [TRUST-A Lite](templates/TRUST-A-LITE.md) before shipping a new agentic workflow or increasing an existing agent's autonomy.

```text
TRUST-A REVIEW

Truth          PASS
Rules          PASS
Uncertainty    WARN
Scope          PASS
Traceability   WARN
Autonomy       PASS

Recommended autonomy: ACT_WITH_APPROVAL

Highest-ROI actions
1. Define freshness requirements for the primary source.
2. Persist tool calls and decision provenance.
```

For a fuller design review, read the [framework](framework/TRUST-A.md).

## When to use TRUST-A

TRUST-A is most useful when an AI workflow:

- reads from multiple or changing sources;
- uses tools or connected systems;
- writes to repositories, databases, SaaS products, or production systems;
- runs automatically or on a schedule;
- makes recommendations that can trigger real-world actions;
- is moving from human-supervised to more autonomous execution.

You probably do **not** need a full TRUST-A review for a simple rewrite, isolated brainstorming session, or low-impact assistant interaction.

## Recommended autonomy ladder

TRUST-A does not assume that maximum autonomy is the goal.

1. **READ_ONLY** — inspect and summarize.
2. **RECOMMEND** — propose decisions or actions without executing them.
3. **ACT_WITH_APPROVAL** — prepare or execute only after an explicit approval gate.
4. **ACT_AUTONOMOUSLY** — execute within a bounded, observable, reversible scope.

Higher consequence and lower reversibility require stronger evidence and tighter controls.

## What is in this repository

```text
trust-a/
├── framework/
│   └── TRUST-A.md
├── templates/
│   ├── TRUST-A-LITE.md
│   └── AGENT-CONTRACT.md
├── skills/
│   └── trust-a-audit/
├── LICENSE
└── README.md
```

### Framework

The canonical explanation of the six dimensions and how they work together.

→ [Read the framework](framework/TRUST-A.md)

### TRUST-A Lite

A short review you can run in a few minutes before shipping or increasing autonomy.

→ [Use TRUST-A Lite](templates/TRUST-A-LITE.md)

### Agent Contract

A reusable template for defining sources of truth, hard rules, stop conditions, capabilities, approval policy, and decision trace.

→ [Use the Agent Contract](templates/AGENT-CONTRACT.md)

### TRUST-A Audit Skill

A reusable AI Skill that audits an agent, workflow, prompt, automation, architecture, or repository instruction set using TRUST-A.

→ [Open the Skill](skills/trust-a-audit/)

## A useful mental model

A common failure mode is to treat an agent as:

```text
Prompt → Model → Action
```

TRUST-A encourages a more explicit system:

```text
Authoritative sources
        ↓
Freshness / validation
        ↓
Deterministic rules
        ↓
Agent reasoning
        ↓
Action preconditions
        ↓
Bounded tool / action
        ↓
Decision trace
```

The model remains important, but reliability comes from the system around it.

## Status

**v0.1 — public foundation**

The framework is intentionally small and will evolve from practical use rather than theoretical completeness. Generic and anonymized use cases will be added over time.

## Contributing

Issues and thoughtful examples are welcome. If you propose a new rule, keep it practical: explain the failure mode it prevents and the smallest control that addresses it.

## License

MIT. See [LICENSE](LICENSE).

---

Created and maintained by [Timothée Olivar](https://github.com/garytopper).