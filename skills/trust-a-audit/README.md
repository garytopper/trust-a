# TRUST-A Audit Skill

An installable AI Skill for reviewing agents, workflows, prompts, automations, architectures, and repository instructions with the TRUST-A framework.

The Skill is intentionally self-contained: once installed, it does not need internet access to understand or apply TRUST-A. When auditing a real system, it should still inspect the actual code, files, tools, runtime evidence, or connected sources that the user authorizes rather than grading from assumptions.

## What it returns

- `PASS / WARN / FAIL / N/A` for each TRUST-A dimension;
- the recommended autonomy level;
- evidence-backed key findings;
- the highest-ROI improvements;
- blockers before increasing autonomy;
- contract-versus-run compliance when runtime evidence is available;
- approval, verification and provenance gaps without turning them into a numeric score.

The Skill also reasons across dimensions rather than treating them as independent checklist items. For example, weak Truth or unresolved Uncertainty should constrain Autonomy, while narrow Scope can reduce the blast radius of model or tool errors.

## Skill structure

```text
trust-a-audit/
├── SKILL.md
├── README.md
├── LICENSE.txt
├── agents/
│   └── openai.yaml
└── references/
    ├── agent-contract.md
    ├── audit-output.md
    ├── risk-autonomy-policy.md
    ├── run-receipt.md
    ├── run-receipt.schema.json
    ├── runtime-oversight.md
    ├── trust-a-framework.md
    └── trust-a-lite.md
```

`SKILL.md` is the control plane: it defines the audit workflow, core reasoning rules, grading behavior, and when to load each reference.

The references provide progressive detail:

- `trust-a-lite.md` — concrete checks for quick or lower-impact reviews;
- `trust-a-framework.md` — the complete TRUST-A mental model, failure modes, controls, and dimension interactions;
- `agent-contract.md` — a remediation template for making sources, invariants, stop conditions, capabilities, approvals, verification and traces explicit;
- `runtime-oversight.md` — contract → execution → verification → receipt → oversight model;
- `risk-autonomy-policy.md` — risk classes, approval defaults and verification expectations;
- `run-receipt.md` / `run-receipt.schema.json` — human and machine-readable runtime evidence contract;
- `audit-output.md` — the default review output shape.

## Example prompts

```text
Run a TRUST-A review on this coding agent before we let it merge pull requests.
```

```text
Audit this automation and tell me what prevents ACT_AUTONOMOUSLY.
```

```text
Apply TRUST-A Lite to this AGENTS.md and prioritize only the three highest-ROI changes.
```

## Canonical docs and bundled references

The public framework and templates remain the canonical sources:

- [`framework/TRUST-A.md`](../../framework/TRUST-A.md)
- [`templates/TRUST-A-LITE.md`](../../templates/TRUST-A-LITE.md)
- [`templates/AGENT-CONTRACT.md`](../../templates/AGENT-CONTRACT.md)
- [`framework/RUNTIME-OVERSIGHT.md`](../../framework/RUNTIME-OVERSIGHT.md)
- [`templates/RISK-AUTONOMY-POLICY.md`](../../templates/RISK-AUTONOMY-POLICY.md)
- [`templates/RUN-RECEIPT.md`](../../templates/RUN-RECEIPT.md)
- [`schemas/run-receipt.schema.json`](../../schemas/run-receipt.schema.json)

The corresponding files under `references/` are generated copies adapted for the standalone Skill package. Do not edit those generated files manually.

After changing a canonical document, regenerate the bundled references from the repository root:

```bash
python scripts/sync-skill-references.py
```

CI runs the same script with `--check` and fails if the Skill package has drifted from the canonical framework.

## Packaging

Package the `trust-a-audit` directory as one Skill bundle for the environment in which you want to install it. The required entrypoint is `SKILL.md`; ChatGPT UI metadata lives in `agents/openai.yaml`.

The Skill is text-only and does not require external connectors by default. External access is useful only when the audit itself requires evidence from a repository, runtime, SaaS product, or other source.

`LICENSE.txt` carries the repository's MIT license with the standalone bundle.
