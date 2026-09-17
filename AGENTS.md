# When starting new repo or no setup-skills-log.md found
- If the repo or project has nothing inside or no setup-skills-log.md is found, always suggest to run /setup-matt-pocock-skills. Even if you are asked to do something else, always notify me in case I forgot and wait for me to respond before trying to do the things I ask you to do. Then log my response for this as setup log, so you wont ask me again in the future.

## Start of session
- Read the newest file in handoffs/ before doing anything else; its "Next session focus" is the plan.
- If running the session outside of a repo, check ~/projects/obsidian-vault/handoffs/ or ~/repos/obsidian-vault/handoffs/ instead.
- 
## Generic Workflow (apply to all kinds of tasks)
- Each sprint follow this cycle. A sprint may be separated by explicitly told or when scope start to deviates from the start.
  - /clear (remove unwanted context)
  - /model (decide model level)
  - Execution (eg.researching, discussing, brainstorming, execution, planning, implementing, etc.)
  - /handoff (write hand off )

## Coding workflow
- Each sprint start with
  - /grill-with-docs (or /wayfinder)
  - /to-spec
  - /to-tickets
  - /implement
- Never implement unless I execute skill /implement


## Agent & Model Allocation Rules

### 1. Model Selection Routing
Choose model execution tiers strictly based on task complexity:
- **`haiku` (Lightweight / Search):**
  - Codebase exploration, directory listing, and file searching.
  - Reformatting, linting, simple regex, and log parsing.
  - Background subagent tasks.
  - Websearch
- **`sonnet` (Default Execution):**
  - Baseline model for all primary coding, refactoring, and file edits.
  - Writing SQL, data pipeline scripts, and analytics tasks.
  - Summarizing research, drafting docs, and routine feature implementations.
- **`opus` / `opusplan` (High-Reasoning Only):**
  - Use `opusplan` for initial architectural planning and multi-system design before executing code.
  - Use `opus` exclusively for complex system debugging, high-stakes edge-case reasoning, or intricate algorithm design where `sonnet` hits a block.
  - **Constraint:** Do not use `opus` for routine file creation, code generation, or read-only tasks.

### 2. Subagent Governance
- **Default Subagent Model:** Subagents must run on `haiku` by default to minimize token usage. Elevate to `sonnet` only if the sub-task involves multi-file refactoring or deep parsing.
- **Concurrency (by conflict, not a fixed count — user, 2026-09-16):**
  - Subagents that write **different files** may run in parallel.
  - Subagents that write the **same files** run one after another, or each in its own git worktree.
  - At most **2 data-heavy subagents** at once (loading full datasets, running notebooks), to protect machine RAM.
  - Soft cap of about **4–5 subagents** at once, to keep token burn and the user's review queue manageable.
  - Only the orchestrator (main session) edits shared tracking files (e.g. KANBAN) and commits.
- **Summary Protocol:** Subagents must return concise summaries or targeted snippets to the main context—never raw file dumps or exhaustive logs.
- **Inline Execution:** For simple, single-file edits or quick lookups, perform the action directly in the main session instead of spawning a subagent.

---


# Andrej Karpathy's Guidelines
Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

## 5. After code is verified, suggest commit before and after major changes are made
- when 
## 6. After a long session (~20-50 prompts), suggest me to run /compact to save token.

## 7. If claude needs to use python, try to see if there already is an environment in .venv. If not create and use this as default environment.

## 8. `wrap` — session wrap-up keyword

When the user types `wrap` (without a slash), perform the following in order before ending the session:
1. If there is any action worth logging, log it so we can refernce
2. Commit and push everything in a single commit and check what has been done and summarize the commit

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.

---
