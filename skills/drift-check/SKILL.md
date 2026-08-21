---
name: drift-check
description: Audit that code, board, branches and docs still agree - detect plan drift before it compounds. Use when the user asks "where are we", "co dalej", "status", asks for a project health check, after returning from a break, roughly at every phase boundary, or whenever docs feel out of date.
---

# Drift check

Read-only audit first, fixes proposed second. Never silently rewrite docs during the audit.

## Audit
1. **Board vs git**: `git log --oneline -30` vs Done section — commits without task IDs? Tasks Done with no corresponding commits? Non-conventional commit subjects that slipped through?
2. **Branch hygiene**: `git branch -a` — merged branches that were never deleted? Branches with no matching task on the board? Work sitting unmerged on a branch while its task says Done?
3. **Code vs ARCHITECTURE.md**: does the real directory tree match the documented one? New top-level dirs, moved modules, adopted libraries not mentioned?
4. **Code vs SPEC.md**: features implemented that aren't in SPEC (scope creep — needs a SPEC entry + decision, or removal)? SPEC features quietly abandoned (move to Out of scope with reason)?
5. **ROADMAP honesty**: does the current phase's exit-criteria checklist reflect reality? Any 🔨 phase actually done or actually stalled?
6. **DECISIONS gaps**: visible in code but never logged — ORM choice, auth approach, folder convention? List them.
7. **Attribution scan**: `git log --format=%B -20 | grep -Ei 'co-authored-by|generated (with|by)|🤖'` and a grep over comments for tool mentions — the rule is only as good as its enforcement.

## Report format
- 🟢 aligned / 🟡 minor drift / 🔴 docs lie about reality — one line verdict
- Findings table: what / where (file, doc, or branch) / proposed fix (one line)
- Then ask which fixes to apply. Batch-apply approved ones, log a `D-xxx` if any fix constitutes a decision.

## Cadence hint
If more than ~10 findings, recommend a dedicated "docs debt" task instead of fixing inline — and add it to Next.
