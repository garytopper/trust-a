# TRUST-A repository instructions

This file is the operational router for work on TRUST-A. The framework itself is canonical under `framework/`; reusable templates live in `templates/`; the packaged audit Skill lives in `skills/trust-a-audit/`.

## Load context by task

- Framework semantics or dimension definitions -> `framework/TRUST-A.md`.
- Runtime authority, verification or oversight -> `framework/RUNTIME-OVERSIGHT.md` and the relevant template.
- Agent/approval/risk contracts -> `templates/`.
- Audit Skill behavior or packaging -> `skills/trust-a-audit/`.
- Public positioning and repository structure -> `README.md`.

Do not duplicate a canonical rule into this file when the owning framework/template already expresses it.

## Repository-wide invariants

- Present TRUST-A as a lightweight engineering/review framework, never as a certification, compliance standard, security product or guarantee.
- Keep examples generic or anonymized unless publication is explicitly approved.
- A runtime/model change must not silently redefine an agent/workflow's authority.
- Preserve the distinction between self-check and independent verification, and between unknown/unobserved evidence and success.
- Changes to canonical framework/templates must keep generated Skill references synchronized via `python scripts/sync-skill-references.py`.

## Workflow and autonomy

- `main` is the only long-lived branch. Use short-lived branches and PRs for non-trivial changes, rebase if needed, squash merge by default, then delete completed branches.
- Work autonomously on scoped reversible repository changes. A request to apply such a change authorizes that class of mutation.
- Stop only when new evidence crosses an unapproved destructive, sensitive-data, permission/security, publication or other difficult-to-reverse boundary.
- Never commit credentials, private conversation exports, unnecessary personal data or internal notes that are not intended for the repository.

## Verification and completion

Run only the checks relevant to the changed surface. When framework/templates change, regenerate bundled Skill references and run the repository's deterministic validation. Do not report independent/runtime/publication evidence that was not actually observed.

A change is complete when canonical sources and generated references remain coherent, relevant checks pass, public wording remains defensible, and the PR records any real uncertainty or unverified evidence.

## AI agent Git identity

For commits made by AI agents on Tim's behalf, configure **repository-local** Git author and committer as `Garytopper <24545329+garytopper@users.noreply.github.com>`. Before each commit, run `git config --local user.name "Garytopper"` and `git config --local user.email "24545329+garytopper@users.noreply.github.com"`; check both effective identities with `git var GIT_AUTHOR_IDENT` and `git var GIT_COMMITTER_IDENT`. Resolve overriding `GIT_AUTHOR_*`/`GIT_COMMITTER_*` environment variables in the actual commit process, then verify the resulting commit. Never change global Git config or rewrite shared history. Full policy: [canonical AI agent Git identity](https://github.com/garytopper/ai-project-instructions/blob/main/shared/repository-execution-policy.md#git-identity-for-tims-coding-agents).
