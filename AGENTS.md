# Project: OpsBeacon

OpsBeacon is a production-style uptime monitoring app for a DevOps / Cloud portfolio: a public demo dashboard, FastAPI backend, PostgreSQL storage, Docker Compose runtime, and Ansible/Nginx deployment path for a single Ubuntu EC2 host.
<!-- This file is the single source of truth for every agent: Codex reads it natively, Claude Code reads it via the CLAUDE.md symlink, Cursor reads it natively (plus .cursor/rules/000-core.mdc points here). Edit THIS file only. -->

## Source of truth

All planning lives in `docs/` — code follows docs, not the other way around:

- `docs/SPEC.md` — what we're building (features, requirements, out-of-scope)
- `docs/ARCHITECTURE.md` — stack, project structure, key technical choices
- `docs/ROADMAP.md` — phases/milestones and their status
- `docs/DECISIONS.md` — decision log (append-only)
- `docs/tasks/TASKS.md` — the working board: Now / Next / Backlog / Done

## Session protocol (non-negotiable)

1. **Start**: read `docs/tasks/TASKS.md`. Work on the task in **Now**. If Now is empty, propose promoting from Next — don't pick silently.
2. **During**: stay inside the task's scope. Discovered work → add to Backlog with a note, don't do it now. Scope grows mid-task → stop, say so, split the task.
3. **Decisions**: any choice that constrains the future (library, schema shape, API contract, naming scheme) → one line in `docs/DECISIONS.md` **in the same turn** you make it.
4. **End of task**: move it to Done with date, update Now/Next, note follow-ups in Backlog. Run `/session-wrapup` before finishing a work session.
5. **Never** mark a task Done if its VERIFY criteria aren't met. Run them and show the evidence.

## Git workflow (non-negotiable)

- **Never commit directly to `main`.** Every task gets its own branch, created from up-to-date main: `git switch main && git pull && git switch -c <type>/T-012-short-slug` (type = feat/fix/chore/docs/refactor).
- **One branch = one task.** Don't smuggle other tasks onto the branch. Branch too big? Split the task first.
- **Conventional Commits**, enforced by the commit-msg hook: subject `type(scope): imperative summary` (lowercase type, ≤72 chars), allowed types: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert. Reference the task in the subject tail or footer: `feat(parser): add offer adapter [T-012]`.
- **After merge, the branch dies**: `git branch -d <branch>` locally and `git push origin --delete <branch>` on the remote. Never reuse a merged branch. No long-lived feature branches.
- Docs updates (TASKS.md, DECISIONS.md) belong in the same commit as the code they describe.
- Significant tasks (integrations, auth, schema, business logic) get a pre-merge review by the OTHER agent: open it on the branch and run `/cross-review`. Blockers are fixed by the author on the same branch before merge.
- Before committing: run the project's test + lint commands (see Commands). Failing checks = no commit, unless the task IS fixing them.
- Never commit secrets, .env files, or generated artifacts; extend .gitignore in the same commit when needed.

## No AI attribution (non-negotiable)

- Never state or imply in any project artifact that content was produced by an AI tool. This means: no "Generated with Claude Code / Codex / Cursor", no `Co-Authored-By: Claude/Codex/agent` trailers, no robot emojis or "AI-assisted" markers — in commit messages, code comments, docstrings, PR titles/descriptions, changelogs, or docs.
- Write comments as a developer would: explain WHY the code is the way it is, never narrate who or what wrote it or the editing process ("updated by...", "as requested...").
- The commit-msg hook rejects attribution trailers as backstop, but the rule applies everywhere, not just commits.

## Scope & verification discipline

- One task at a time. If implementing T-x reveals that T-y is needed first, stop and say so — don't silently do both.
- Refactors, renames, and "while I'm here" improvements outside the current task's files → Backlog, not now.
- A task's VERIFY line is a contract: run it, paste the evidence (test output, response body) before moving the task to Done.
- Broken main is priority zero: if tests/build fail on main, fixing that outranks the Now task.
- If code and docs disagree, STOP and ask which is right — then fix the loser. Never silently follow one.
- Uncertain about intent (spec ambiguous, two valid readings)? Ask with a concrete A/B, don't pick silently.

## Commands

- `make up` — start the local Docker Compose stack
- `make down` — stop the local stack
- `make logs` — follow service logs
- `make test` — run pytest
- `make lint` — run Ruff
- `make migrate` — apply Alembic migrations
- `make seed` — insert demo monitors idempotently
- `docker compose config` — validate local Compose config
- `ansible-playbook -i ansible/inventory.example.ini ansible/playbook.yml --syntax-check` — validate Ansible syntax

## Conventions

- V1 has no login; all routes are public demo routes.
- HTTP monitoring logic lives in `app/services/`, not route handlers.
- Database access is synchronous SQLAlchemy 2.x sessions.
- URL validation must reject non-HTTP(S), localhost, link-local, and private/internal IP literals.
- Tests must mock outbound HTTP checks; no live third-party dependency in CI.
- Demo seed data must be idempotent.
- Docker runtime runs as a non-root user.
- V2 infrastructure belongs in docs only until a future task.
