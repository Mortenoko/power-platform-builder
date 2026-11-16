# Building on the Power Platform with Claude: the short guide

## The idea

Claude can build and change Power Apps, Power Automate flows, Copilot Studio agents and Dataverse through MCP tools and the Power Platform CLI. You describe what you want and review the result. The agent does the repetitive work. You keep control over what goes live.

What makes it work is not the tools alone but a **method**:

1. **Know where you are.** Confirm tenant, account, environment and solution before the first change.
2. **Gates for anything outward-facing.** Publish, send, delete and permission changes need a clear yes from a person each time.
3. **Solution-first, source in the repo.** Everything lives in a solution and is exported after each publish, so the repo is the record.
4. **Small verified steps.** Change, compile, look, then move on. Say what was tested and what was not.
5. **A backlog the agent can read**, with acceptance criteria and a ready flag.

## What each surface is good for

| Surface | Claude builds | Watch out for |
|---|---|---|
| Canvas app | Screens, Power Fx, data binding | Session expiry, layout order, preview staleness |
| Flows | Cloud flows as code with connection references | Test with new records, notification side effects |
| Copilot Studio | Agents, workflows, knowledge | Inconsistent file output, review before publishing |
| Dataverse | Tables, columns, roles, data | Prefix is permanent, link tables, migrations |

## A typical session

1. Open the project; `CLAUDE.md` states the environment and rules.
2. Pick a ready backlog item. Claude restates the acceptance criteria.
3. Claude builds in the dev environment and shows the result.
4. You review. Claude fixes, then asks before publishing.
5. After publish, Claude exports the solution and updates the README and the backlog note.

## Getting started

1. Install the plugin and run the `setup` skill. For canvas apps, **enable co-authoring on the app in Studio (Settings, General) and save it** before Claude connects; this is a manual step only you can do.
2. Run `project-starter` in a new folder.
3. Start with a small, real item and follow the gates.

## Good habits

- Write the surprises into `CLAUDE.md` as lessons learned.
- Keep one source of truth for the schema.
- Prefer idempotent scripts with a dry run.
- Never paste secrets into a chat or a file.
