# Project collaboration

This repository contains the AI Usage Telemetry Platform portfolio project and its learning plan.

- Read this file, docs/CONTEXT.md, docs/PROGRESS.md and docs/LEARNING_PLAN.md before continuing project work. Read docs/DEVELOPMENT.md before running commands.
- The current Codex chat is the main learning conversation. Repository documents carry progress between computers and chats.
- Explain in Russian using simple, respectful language. Teach one small step at a time; continue when the user says «дальше».
- Build on the user's existing Data Engineering experience. Explain AI concepts, engineering trade-offs and concrete failure cases.
- Prepare infrastructure, lab scaffolding and meaningful checks autonomously when requested. Let the user implement core exercise logic with hints unless they request implementation.
- Distinguish discussed topics from independently demonstrated skills. Do not mark a skill mastered merely because agent-written tests pass.
- Update docs/PROGRESS.md after meaningful learning or implementation checkpoints. Record evidence and the next step.
- Use synthetic data, keep credentials out of Git, and identify simulated incidents and unimplemented features explicitly.
- Keep the project incremental. Verify current official documentation before implementing evolving integrations.
- Use small commits and codex/* branches for subsequent development. Check working-tree state before changing branches or pulling; preserve existing work.
- Public README is in English; learning documents may be in Russian.

## Portable handoff

- These instructions apply to any coding assistant working in this repository. Do not depend on chat memory, a provider-specific integration or a particular local path.
- Keep confirmed facts and learning preferences in docs/CONTEXT.md, current results and next actions in docs/PROGRESS.md, and reproducible setup in docs/DEVELOPMENT.md.
- Before editing, inspect git status, the current branch, recent commits and relevant files. Preserve uncommitted work and do not reset, clean, force-push or switch away from it without resolving ownership.
- Read progress as context, not proof: verify actual files and test results. If a document contradicts the repository, report and correct it based on evidence.
- For each handoff, record the branch, commands and outcomes, deliberate unfinished exercises, blockers and one concrete next action. Do not store tokens, device codes, secrets or full private chat transcripts.
- Never mark an exercise completed solely because infrastructure tests pass. Starter exercises may deliberately raise NotImplementedError; report these separately from regressions.
- Use .venv for project dependencies. Document portable commands rather than hard-coding the original computer's runtime paths. Installing or enabling a tool on one PC does not configure another PC automatically.
- Make a commit/push when requested or authorized by the ongoing task. Verify the remote ref and clean working tree before claiming changes were synchronized. Keep main stable; publish development branches for cross-computer continuation.
- If your client does not automatically load AGENTS.md, explicitly read it before working. Other assistants need no separate copy of these instructions.
