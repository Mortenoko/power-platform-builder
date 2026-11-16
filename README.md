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

## Install

Add this folder or its git repository as a plugin marketplace, then install `power-platform-builder`:

```
/plugin marketplace add <path-or-git-url>
/plugin install power-platform-builder@power-platform-builder
```

Companion plugins needed for the actual authoring: the canvas apps, Dataverse and Copilot Studio plugins from Microsoft (see the `setup` skill).

## Scope

Method and lessons only. No customer data, tenant names, ids or credentials belong in this repository.

## Status

Version 0.1.0, first draft. Written from a real build; not yet tested by other people.
