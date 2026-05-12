# GitHub Copilot Workspace Instructions

## Workspace status
- This repository currently has no source files, documentation, or build metadata.
- Use this file as the primary workspace instruction guide until project-specific conventions are added.

## How to behave
- If the user asks for code, first confirm the target language, framework, and desired output structure when it is not already clear.
- If the repository is empty, prefer scaffolding a sensible starting point rather than guessing project details.
- When asked to implement features, ask for missing requirements or sample inputs if the request is underspecified.

## When adding files
- Keep files and folder names simple and idiomatic for the chosen platform.
- Prefer standard project layouts for common stacks (for example, `src/`, `tests/`, `package.json` for Node; `app/`, `requirements.txt` for Python).
- Add documentation entries only when the repository contains actual implementation details.

## Communication style
- Keep answers short, focused, and actionable.
- Use headings and bullet lists for clarity.
- When the workspace lacks context, explain that the repository appears empty and ask the user how they want to proceed.

## Next steps for this workspace
- Add a `README.md` or project scaffold so the agent can learn architecture and build/test commands.
- Once sources exist, update this file with stack-specific conventions, scripts, and important files.
