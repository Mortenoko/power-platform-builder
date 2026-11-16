# Power Platform Builder

A Claude Code plugin with a working method for building **Power Apps, Power Automate flows, Copilot Studio agents and Dataverse solutions** with Claude through MCP tools. It adds method, approval gates, environment safety and hard-won lessons on top of Microsoft's own plugins; it does not replace them.

## Skills

| Skill | Use it for |
|---|---|
| `setup` | Install tools, connect the MCP servers, sign in, verify |
| `method` | The shared operating method and approval gates (read first) |
| `canvas-apps` | Canvas authoring loop, layout, Power Fx and data lessons |
| `flows` | Flows as code, connection references, testing |
| `copilot-studio` | Agents and workflows, choosing the right building block, testing |
| `dataverse` | Schema as code, solution-first, migration, roles, export |
| `project-starter` | New project structure, `CLAUDE.md` and architecture templates |

Read `docs/guide.md` for the two-page overview.

`scripts/` holds small, dependency-free helpers: `deploy_schema.py` (idempotent Dataverse schema from a JSON file, dry run by default), `flow_tool.py` (create, update, turn on, run and inspect a flow) and `dv.py` (token and Web API helper). They need `DATAVERSE_URL` and `az login`.

## Install

Add this folder or its git repository as a plugin marketplace, then install `power-platform-builder`:

```
/plugin marketplace add <path-or-git-url>
/plugin install power-platform-builder@power-platform-builder
```

Then install Microsoft's companion plugins, which do the actual authoring (this plugin adds method on top and does not duplicate them):

```
/plugin marketplace add microsoft/power-platform-skills
/plugin install canvas-apps@power-platform-skills
/plugin marketplace add microsoft/Dataverse-skills
/plugin install dataverse@dataverse-skills
/plugin marketplace add microsoft/skills-for-copilot-studio
/plugin install copilot-studio@skills-for-copilot-studio
```

Restart Claude Code, then ask Claude to run the `setup` skill.

## Prerequisites

Git, Python 3, the Power Platform CLI (`pac`), the .NET 10 SDK (canvas authoring MCP), the Azure CLI (`az`, used for API tokens in the scripts), and a Power Platform environment you may change. A work account in that tenant is needed for sign-in. Use a dev or sandbox environment.

Two things cannot be done from code and need you: **sign-in and consent**, and **enabling co-authoring on a canvas app** (Studio, Settings, General), plus publishing.

## Scope

Method and lessons only. No customer data, tenant names, ids or credentials belong in this repository.

## Status

Version 0.1.0, first draft. Written from a real build; not yet tested by other people.
