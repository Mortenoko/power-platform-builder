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
| Azure CLI | `az --version`, `az account show` | API tokens for the scripts (same account as `pac`) |
| Node | `node --version` | browser-console scripts and flow builders (optional) |

## 2. Companion plugins (do not duplicate them)

This plugin adds method and lessons on top of Microsoft's own tooling. Install what you need:

- Canvas apps: `/plugin marketplace add microsoft/power-platform-skills`, then `/plugin install canvas-apps@power-platform-skills` (the Canvas Authoring MCP).
- Dataverse: `/plugin marketplace add microsoft/Dataverse-skills`, then `/plugin install dataverse@dataverse-skills`.
- Copilot Studio: `/plugin marketplace add microsoft/skills-for-copilot-studio`, then `/plugin install copilot-studio@skills-for-copilot-studio` (includes the MCP bridge).
- Restart Claude Code after installing so the MCP servers load. Check `claude plugin list`.
- Optional: a browser extension or built-in browser so Claude can use Studio and admin pages.

## 3. Sign in and pick the environment

1. `pac auth list` then `pac org who`. Confirm the environment URL and account with the user.
2. If the environment is in another tenant or region, or is brand new, create a new auth profile instead of reusing one. A new environment may be missing from `pac env list` for a while, so connect by full URL: `pac auth create --name <profile> --environment https://<org>.<region>.dynamics.com`, then `pac org who` and compare name, URL and account with what the user said. An old profile often points at a different environment.
3. For scripts that call the Dataverse or Power Automate Web APIs, a token from the Azure CLI works (`az account get-access-token --resource <environment URL>`; for flows use `https://service.flow.microsoft.com/`). Check `az account show` is the same account.
4. Record the environment URL, environment id, solution name and publisher prefix in the project `CLAUDE.md` (see `project-starter`).

## 4. Connect each authoring surface

- **Canvas app:** **co-authoring must be enabled for the app.** This is a per-app setting that the user turns on in Power Apps Studio (Settings, then General; scroll down if needed), then saves the app. Without it `connect` fails with "Coauthoring is not enabled for this app". Claude cannot reliably do this for the user, so ask them to do it and wait for confirmation.
  - The app must be saved at least once (a new blank app has no app id and `sync_canvas` returns no files). Get the app id from the Studio URL or the Power Apps app list.
  - Keep exactly one Studio tab open on the app; a second tab opens read-only and blocks editing. The tab must stay open for the whole session.
  - Call `connect` with environment id, app id and the account. If sync fails with no detail, the Studio session expired: reload Studio in a fresh tab, then connect again.
- **Dataverse:** use the Python SDK for scripts and the Dataverse MCP for small reads and writes (see `dataverse`).
- **Copilot Studio:** check status, sign in through the bridge (the browser prompt is the user's click), list and select the environment the user named, then load the newly available tools (`manage_agents`, `discover_resources`, the skill reader) before authoring. Read the bridge's own authoring guidance before composing a definition.
- **Connections:** the Copilot Studio bridge can create connections: prepare a plan (it writes nothing), show the user the connector, environment and account, and only after a clear yes run the setup. Verify the connection shows Connected.

## 5. Verify

Do one harmless read through each connection (list data sources, list tables, list agents). Report which work and which do not, with the exact fix for each.

## Things that trip people up

- A table, column or connection created after Studio opened is not visible until you save, open Studio in a fresh tab and reconnect.
- Old tabs with unsaved changes block navigation ("Leave site?"). Open a new tab instead of forcing it. A second Studio tab on the same app opens read-only until the first is closed.
- Co-authoring cannot be switched on from code: it is not in the app resource of the Power Apps API or in the downloaded app file (tested). Ask the user.
- Do the rest from code where a route exists; send the user to the portal only for sign-in, consent, enabling co-authoring, first save of a new canvas app and publishing.
- Never click through consent or sign-in prompts on someone's behalf; ask them.
