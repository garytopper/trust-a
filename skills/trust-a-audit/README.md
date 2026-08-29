# TRUST-A Audit Skill

An installable AI Skill for reviewing agents, workflows, prompts, automations, architectures, and repository instructions with the TRUST-A framework.

## What it returns

- `PASS / WARN / FAIL / N/A` for each TRUST-A dimension;
- the recommended autonomy level;
- evidence-backed key findings;
- the highest-ROI improvements;
- blockers before increasing autonomy.

## Skill structure

```text
trust-a-audit/
├── SKILL.md
├── agents/
│   └── openai.yaml
└── references/
    └── audit-output.md
```

The folder follows the Agent Skills / ChatGPT Skill structure and can be packaged as a ZIP for import into compatible environments.

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

## Packaging

If you use OpenAI's Skill tooling, package the `trust-a-audit` directory as a single Skill ZIP. The required entrypoint is `SKILL.md` and the UI metadata lives in `agents/openai.yaml`.

The Skill is intentionally text-only and does not require external connectors by default. When auditing real systems, the assistant should inspect the actual files, architecture, repository, or connected sources the user authorizes rather than grading from assumptions.
