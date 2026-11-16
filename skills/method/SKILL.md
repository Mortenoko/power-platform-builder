---
name: method
description: The working method for any Power Platform build with Claude: environment safety, approval gates, solution-first, source in the repo, definition of done. Use at the start of any task that creates or changes a Power App, flow, Copilot Studio agent or Dataverse component, and whenever a change would publish, send, delete or change permissions.
---

# Power Platform build method

This is the shared operating method. The surface skills (`canvas-apps`, `flows`, `copilot-studio`, `dataverse`) add the technical detail. Follow this first.

## 1. Know where you are before you change anything

- State the **tenant, account, environment and solution** you will touch, and have the user confirm them once per session. Run `pac org who` (or the equivalent) and compare it with what the user said. Never trust an auth profile, a `.env` file or a previous session.
- Several accounts are often signed in to the same browser. Use the account the user named in every sign-in, picker and tool. Never pick another.
- Prefer a dev or test environment. Production changes go through a pipeline or an exported solution, not by hand.

## 2. Approval gates (ask, wait for a clear yes)

Always ask first, even if the work was requested in general terms:

- Publishing an app or flow, or turning a flow on.
- Sending messages or email, or any write that notifies other people.
- Changing site permissions, sharing, roles or security settings.
- Deleting data or components that cannot be recovered.
- Granting consent, OAuth or connection prompts, or entering credentials.

An approval covers one action. A "publish" yes does not cover the next publish.

## 3. Build solution-first, source in the repo

- Everything lives in a **solution** with a publisher prefix you chose on purpose (the prefix is permanent).
- Make the change in the environment through the API or MCP tool, then **export and unpack the solution into the repo**. Do not hand-write solution XML for new components.
- Keep generators and scripts in the repo or a scratch folder, not pasted into chat. Prefer idempotent scripts with a dry-run switch.
- Keep the schema as code (one file is the source of truth), and make the README match every change.

## 4. Work in small verified steps

- Change a little, compile or validate, then look at the result (screenshot, sync to a scratch folder, test run).
- A tool saying "failed" may still have applied part of the change; verify the state instead of assuming.
- Never claim something works that you have not run. Say what was tested and what was not.
- Sub-agents usually cannot use the authoring MCP tools; do the editing and syncing in the main session.

## 5. Definition of done

1. The requirement or acceptance criteria are met.
2. The app compiles, the flow validates or ran once end to end, the agent answered a test prompt.
3. The solution is exported and the repo matches the environment.
4. Documentation matches (README, schema file, backlog item).
5. The user is told exactly what to refresh, reload or publish, and what is **not** tested.

## 6. Keep a backlog the agent can read

Use a simple list with an ID, status, description, acceptance criteria and a "ready for dev" flag. Pick up only ready items, and write progress notes back to the item.
