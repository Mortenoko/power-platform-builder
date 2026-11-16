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

`scripts/` holds small, dependency-free helpers: `doctor.py` (read-only machine check Claude runs during setup), `deploy_schema.py` (idempotent Dataverse schema from a JSON file, dry run by default), `flow_tool.py` (create, update, turn on, run and inspect a flow) and `dv.py` (token and Web API helper). The Dataverse and flow scripts need `DATAVERSE_URL` and `az login`; `doctor.py` needs neither.

## Install

Add the four marketplaces (this plugin plus Microsoft's three), then install this plugin. It declares the Microsoft plugins as dependencies, so one install brings in all four. Run these in any terminal (this works for the Claude Code desktop app too, where typing `/plugin ...` only opens the plugin window):

```bash
claude plugin marketplace add Mortenoko/power-platform-builder
claude plugin marketplace add microsoft/power-platform-skills
claude plugin marketplace add microsoft/Dataverse-skills
claude plugin marketplace add microsoft/skills-for-copilot-studio
claude plugin install power-platform-builder@power-platform-builder
```

In the terminal Claude Code you can type the same as slash commands instead: `/plugin marketplace add <repo>` and `/plugin install power-platform-builder@power-platform-builder`.

The Microsoft marketplaces must be added first: Claude Code does not add them for you, and the install fails with "Is the marketplace added?" if one is missing. The plugins that come with it are `canvas-apps`, `dataverse` and `copilot-studio`; they do the actual authoring and this plugin adds method on top without duplicating them.

Restart Claude Code, then ask Claude to run the `setup` skill. To install from a local folder instead, use the folder path in the first command.

## Getting set up

After installing, restart the app and say **"set me up for Power Platform"** (or `/power-platform-builder:setup`). Claude checks your machine, installs missing tools after asking you once, installs any missing companion plugin, and signs in only to what you are about to use. You click the browser sign-in prompts; Claude does the rest.

What you may need on the machine, depending on what you build (Claude checks and offers to install these): git, the Power Platform CLI (`pac`), the .NET 10 SDK (canvas apps only), and optionally Python and the Azure CLI for the helper scripts. Use a dev or sandbox environment.

Things that cannot be done from code and need you: **sign-in and consent**, **enabling co-authoring on a canvas app** (Studio, Settings, General), and **publishing**.

## Scope

Method and lessons only. No customer data, tenant names, ids or credentials belong in this repository.

## Status

Version 0.1.0, first draft. Written from a real build; not yet tested by other people.
