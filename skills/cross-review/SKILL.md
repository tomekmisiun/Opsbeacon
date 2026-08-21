---
name: cross-review
description: Pre-merge review of the current task branch, designed to be run by a DIFFERENT agent than the one that wrote the code (Codex reviews Claude's work or vice versa) for uncorrelated blind spots. Use when the user asks for a review of a branch/PR, says "zrób review", "cross review", "sprawdź ten branch", or before merging a significant task (new integration, auth, schema, scoring/business logic).
---

# Cross review

You are the reviewer, not the author. You have NO access to the author's conversation — by design. Everything you need is in the repo: the diff, `AGENTS.md`, `docs/`, and the task's VERIFY line. Judge the artifact, not the intent.

## Scope check first
Trivial diffs (dep bumps, typo fixes, pure docs) don't need this ceremony — say so in one line and stop. Review properly when the task touches: external integrations, auth/permissions, data schema, money/scoring/business logic, security-sensitive paths, or >200 changed lines.

## Procedure
1. **Anchor**: identify the task — `git branch --show-current` maps to `T-xxx` on `docs/tasks/TASKS.md`. Read its VERIFY line, the related SPEC feature, and any DECISIONS entries touching this area.
2. **Diff**: `git fetch origin main` (if remote exists) then `git diff main...HEAD` and `git log main..HEAD --oneline`. Review the diff, opening surrounding files where context matters — never judge a hunk blind.
3. **Check, in priority order**:
   - **Correctness vs task**: does the change actually satisfy the VERIFY line? Anything claimed done but untested?
   - **Scope**: changes unrelated to T-xxx smuggled onto the branch? (Board rule: one branch = one task.)
   - **Convention violations**: against AGENTS.md Conventions/Commands and any nested AGENTS.md in touched directories.
   - **Correctness in general**: logic errors, edge cases, error handling, race conditions, N+1s.
   - **Security**: injection, authz gaps on new endpoints/queries, secrets, unsafe input handling.
   - **Tests**: new logic without tests, tests that assert nothing, mocks hiding the thing under test.
   - **Docs sync**: TASKS.md/DECISIONS.md updated in this branch as the workflow requires?
   - **Policy**: commit subjects conventional, no AI attribution in messages or comments.
4. **Report** (in chat, nothing written to files):
   - One-line verdict: ✅ merge / 🟡 merge after fixes / 🔴 needs rework
   - Findings grouped **Blocker / Should fix / Nit**, each as `file:line — problem — suggested fix (one line)`
   - If clean: say so briefly and name the two riskiest spots you checked, so the author knows coverage wasn't superficial.

## Rules
- Review only — do NOT edit code, commit, or update the board. Fixes belong to the author (the other agent) on the same branch; re-run cross-review after Blockers are addressed.
- No style nitpicking that a formatter/linter should catch — if it bothers you, the finding is "add the lint rule", not 30 nits.
- Verify claims yourself where cheap: run the test/lint commands from AGENTS.md → Commands instead of trusting green checkmarks in the description.
