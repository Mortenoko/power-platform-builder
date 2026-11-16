---
name: setup
description: Set up Claude to build on the Power Platform: install tools, connect the MCP servers for canvas apps, Dataverse and Copilot Studio, sign in with the right account, and verify each connection. Use when someone is new to this, a connection is missing or "not connected", or a session has expired.
---

# Setup: connect Claude to the Power Platform

Run these checks in order, skip what already works, and stop at the first failure.

## 1. Tools

| Need | Check | Used for |
|---|---|---|
| Git | `git --version` | source control |
| Python 3 | `python3 --version` | Dataverse scripts (SDK) |
| Power Platform CLI | `pac` | environment, solution export/import |
| .NET 10 SDK | `dotnet --list-sdks` | the canvas authoring MCP server |
| Node | `node --version` | browser-console scripts and flow builders (optional) |

## 2. Companion plugins (do not duplicate them)

This plugin adds method and lessons on top of Microsoft's own tooling. Install what you need:

- Canvas apps: the Canvas Authoring MCP plugin (`canvas-apps`).
- Dataverse: the `dataverse` plugin (skills and the Dataverse MCP).
- Copilot Studio: the `copilot-studio` plugin and its MCP bridge.
- Optional: a browser extension or built-in browser so Claude can use Studio and admin pages.

## 3. Sign in and pick the environment

1. `pac auth list` then `pac org who`. Confirm the environment URL and account with the user.
2. If the environment is in another tenant or region, create a new auth profile instead of reusing one.
3. Record the environment URL, environment id, solution name and publisher prefix in the project `CLAUDE.md` (see `project-starter`).

## 4. Connect each authoring surface

- **Canvas app:** the app must be open in Power Apps Studio with co-authoring on, and the browser tab must stay open. Call `connect` with environment id, app id and the account. If sync fails with no detail, the Studio session expired: reload Studio in a fresh tab, then connect again.
- **Dataverse:** use the Python SDK for scripts and the Dataverse MCP for small reads and writes (see `dataverse`).
- **Copilot Studio:** sign in through the bridge, select the environment, and refresh the tool list before authoring.

## 5. Verify

Do one harmless read through each connection (list data sources, list tables, list agents). Report which work and which do not, with the exact fix for each.

## Things that trip people up

- A table, column or connection created after Studio opened is not visible until you save, open Studio in a fresh tab and reconnect.
- Old tabs with unsaved changes block navigation ("Leave site?"). Open a new tab instead of forcing it.
- Never click through consent or sign-in prompts on someone's behalf; ask them.
