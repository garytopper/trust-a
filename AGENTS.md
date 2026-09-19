# TRUST-A agent instructions

Keep this file short and operational. The canonical framework lives in `framework/`; reusable templates live in `templates/`; the packaged audit skill lives in `skills/trust-a-audit/`.

## Repository workflow

- `main` is the reference branch and the only long-lived branch.
- Start non-trivial work from the latest `main` on a short-lived `feat/*`, `fix/*`, `docs/*`, `chore/*` or `refactor/*` branch.
- If `main` advances before merge, rebase onto the latest `main` and rerun affected validation.
- Target `main` with PRs and squash merge by default. The resulting commit uses Conventional Commits and includes `(#<issue>)` when applicable.
- Delete completed branches after merge; do not introduce permanent `develop`, `preprod`, `preview` or `staging` branches without a documented technical need.
- Keep CI deterministic and lightweight; generated Skill references must remain synchronized with their canonical framework/templates.
- Never commit credentials, private conversation exports, unnecessary personal data or internal working notes intended to stay private.

## Content rules

- Do not present TRUST-A as a certification, compliance standard, security product or guarantee.
- Changes to canonical framework/templates must keep bundled Skill references synchronized via `python scripts/sync-skill-references.py`.
- Keep examples generic/anonymized unless their publication is explicitly approved.
- Do not duplicate the same canonical rule across several sources unless one is a generated artifact with validation.

<!--
Shared execution policy v1.0.0
Canonical source: https://github.com/garytopper/ai-project-instructions/blob/main/shared/execution-policy.md
-->
## Shared execution policy

Ask for clarification only when missing information could materially change the scope, architecture, strategy, or expected result.

For non-blocking ambiguity, infer a reasonable default from the repository, issue, documentation, conversation context, and existing conventions, then proceed.

When implementation or execution is requested, continue until the requested outcome is complete. Do not stop at analysis, a plan, a first draft, or a partial implementation.

Before finishing, run the relevant checks, inspect the result when possible, fix issues found, and verify the acceptance criteria or expected outcome.

Stop only for a genuine blocker, missing required access, a safety constraint, or an irreversible or materially consequential decision requiring human approval.

More specific repository, project, domain, or safety instructions take precedence over this shared baseline.
