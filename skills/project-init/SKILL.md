---
name: project-init
description: Interview-driven initialization of a new project - fills AGENTS.md, docs/SPEC.md, ARCHITECTURE.md, ROADMAP.md and the first tasks in TASKS.md, and wires git hooks. Use when the user starts a fresh project, says "zainicjuj projekt" / "init project" / "let's start", describes an app idea in an empty repo, or when docs/ still contains unfilled template placeholders.
---

# Project init

Goal: leave the repo with docs filled well enough that any future session — in any agent — can work from them alone. Interview → propose → fill. Never fill docs with guesses presented as facts.

## 1. Interview (batch questions, don't interrogate one-by-one)
Round 1 — product: what problem, for whom, the 3-5 core features, what's explicitly NOT in v1, constraints (time, money, hosting, legal).
Round 2 — technical: user's strongest languages/frameworks, existing code/foundations to reuse, deployment target, solo or team.
If the conversation already contains answers, extract them and only ask about gaps — confirm your extraction instead of re-asking.

## 2. Propose before writing
Present: recommended stack (with one honest alternative and the tradeoff), phase breakdown (Phase 0 = walking skeleton: the whole stack runs end-to-end doing almost nothing), and the first 3-5 tasks of Phase 0. Get a yes.

## 3. Fill the docs (in this order)
1. `docs/SPEC.md` — from round 1. Every feature gets a verifiable "works means" sentence.
2. `docs/ARCHITECTURE.md` — stack WITH versions, real directory tree you intend to create, key flows.
3. `docs/ROADMAP.md` — phases with 3-7 exit criteria each. Phase 0 first.
4. `docs/DECISIONS.md` — log D-001 (stack choice, with rejected alternative) and any other decisions made during init.
5. `docs/tasks/TASKS.md` — first task into Now, 3-4 into Next, rest of Phase 0 into Backlog. Every task has a VERIFY line.
6. `AGENTS.md` — project name, one-paragraph description, Commands section (real commands for the chosen stack), 5-10 hard conventions. Remove all `<!-- FILL -->` markers. Do NOT touch the Git workflow / No AI attribution / Session protocol sections — they are fixed policy.

## 4. Wire the repo
- `git init` if needed; then enable the shared hooks: `git config core.hooksPath scripts/git-hooks` (this enforces Conventional Commits and the no-attribution rule for every tool).
- Create a starter `.gitignore` for the chosen stack (env files, build artifacts, IDE junk, caches).
- Extend agent permissions with the project's test/lint/typecheck commands: `.claude/settings.json` allow-list; mention that Codex users may want matching granular approvals.
- Area-specific conventions → nested `AGENTS.md` in the relevant subdirectory (e.g. `backend/AGENTS.md`), not more root-file bloat.
- Fill the three placeholder commands in `.github/workflows/ci.yml` (Lint/Typecheck/Test) with the same real commands as AGENTS.md → Commands.
- Recommend to the user (can't be done from CLI): enable branch protection on `main` in the repo settings — require PRs, block direct pushes; and install `gitleaks` locally so the pre-commit secret scan is active.
- First commit on main is allowed ONLY for this scaffold: `chore: initialize project scaffold [T-000]`. Everything after runs branch-per-task.

## 5. Close
Summarize what was written where, state the Now task and its branch name (`<type>/T-001-slug`). Offer to create the branch and start.
