---
name: setup
description: Set up Claude to build on the Power Platform, doing as much as possible itself: check the machine, install missing tools (after asking), install companion plugins, sign in only to what the task needs, and verify each connection. Use when someone is new to this, says "set me up", a tool or connection is missing or "not connected", or a session has expired.
---

# Setup: Claude does it, the user only clicks

You do the work. Ask the user only for what has no code route: **sign-in clicks, consent, enabling co-authoring on a canvas app, and publishing**. Set up only the surface the user is about to use; do not sign in to everything.

## 1. Find out what they are building

Ask one question if it is not clear: Dataverse tables and data, a flow, a canvas app, a Copilot Studio agent, or several. Then use this table to decide what to check and which sign-ins to expect, and **tell the user up front how many sign-in prompts to expect**.

| Surface | Tools needed | Sign-ins |
|---|---|---|
| Dataverse, solutions | git, `pac` (needs .NET) | `pac auth` (browser) |
| Flows | the first row, plus Node.js 18+ and the Azure CLI (Microsoft's `power-automate` plugin) | `pac auth`, `az login` |
| Canvas app | the first row, plus .NET 10 SDK | `pac auth`, canvas authoring MCP (browser), Studio open in one tab, co-authoring on |
| Copilot Studio agent | none beyond the plugin | bridge sign-in (browser) |

## 2. Check the machine in one call

Run the plugin's read-only status script and read the result. Find it in the installed plugin folder, then run it with the Python you have (`python3` on Mac and Linux; `python` or `py` on Windows; add `--json` to parse it):

```bash
find ~/.claude/plugins -name doctor.py -path "*power-platform-builder*"
python3 <path-to>/doctor.py --json
```

```powershell
Get-ChildItem -Recurse "$env:USERPROFILE\.claude\plugins" -Filter doctor.py | Where-Object FullName -like "*power-platform-builder*"
python <path-to>\doctor.py --json
```

If there is no Python at all, skip the script and check each tool by hand (`git --version`, `pac help`, `dotnet --list-sdks`, `az --version`, `node --version`), then install Python first. On a Mac, a missing `git` or `python3` can open the Xcode command line tools dialog: tell the user to accept it and wait.

It reports the OS, which tools are installed and versions, the active `pac` environment, the Azure CLI account, and which Claude Code plugins are installed, with an install command for every missing tool on this OS.

## 3. Install what is missing, with one approval

List the missing tools and their install commands and ask **once** for approval to run them (for example `brew install dotnet`, `dotnet tool install --global Microsoft.PowerApps.CLI.Tool`, `winget install Microsoft.AzureCLI`). Run them, then run the status script again. If a tool is installed but not found, the PATH is stale: tell the user to restart the terminal or app. `pac` installed with `dotnet tool install --global` lives in `~/.dotnet/tools` (`%USERPROFILE%\.dotnet\tools` on Windows), which must be on the PATH; add it if it is not. A missing package manager (Homebrew on Mac, winget on Windows) must be installed first. Only install what the chosen surface needs.

## 4. Install the companion plugins

This plugin depends on Microsoft's `canvas-apps`, `dataverse`, `copilot-studio` and `power-automate` plugins and does not duplicate them; installing this plugin normally brings them in. If the status script lists one as missing, add its marketplace and install it (ask first; the user must restart the app afterwards so the MCP servers load):

```bash
claude plugin marketplace add microsoft/power-platform-skills   && claude plugin install canvas-apps@power-platform-skills
claude plugin marketplace add microsoft/Dataverse-skills        && claude plugin install dataverse@dataverse-skills
claude plugin marketplace add microsoft/skills-for-copilot-studio && claude plugin install copilot-studio@skills-for-copilot-studio
claude plugin install power-automate@power-platform-skills
```

If the `claude` command is not found (it can be missing from the PATH when only the desktop app is installed), use the app's plugin window to add the same marketplaces and install the same plugins. Tell the user the Power Automate plugin sends pseudonymous usage metadata by default and can be switched off with `/power-automate:telemetry off`.

## 5. Sign in and pick the environment

1. `pac auth list` then `pac org who`. Confirm environment URL and account with the user.
2. If the environment is in another tenant or region, or is brand new, create a new auth profile instead of reusing one. A new environment may be missing from `pac env list` for a while, so connect by full URL: `pac auth create --name <profile> --environment https://<org>.<region>.dynamics.com`, then `pac org who` and compare name, URL and account with what the user said. An old profile often points at a different environment. The browser prompt is the user's click; run the command and tell them to complete it.
3. Scripts that call Web APIs get tokens from the Azure CLI (`az account get-access-token --resource <environment URL>`; for flows `https://service.flow.microsoft.com/`). That needs `az login` with the same account. No Azure subscription or Azure role is needed: the token is for the Power Platform environment, so sign in with `az login --allow-no-subscriptions --tenant <tenant id or domain>` and, if a subscription picker still appears, choose any entry (it is not used) and never ask the user to use someone else's subscription. What the scripts may do comes from the user's own roles in the environment. In some tenants an admin must consent to the Azure CLI. If it is blocked, use the Dataverse plugin, the Dataverse MCP and `pac` instead of the scripts.
4. Record environment URL, environment id, solution name and publisher prefix in the project `CLAUDE.md` (see `project-starter`).

## 6. Connect the surface

- **Canvas app:** **co-authoring must be enabled for the app.** The user turns it on in Power Apps Studio (Settings, then General; scroll down if needed) and saves the app. Without it `connect` fails with "Coauthoring is not enabled for this app". Ask them to do it and wait for confirmation.
  - The app must be saved at least once (a new blank app has no app id and `sync_canvas` returns no files). Get the app id from the Studio URL or the Power Apps app list.
  - Keep exactly one Studio tab open on the app; a second tab opens read-only and blocks editing. The tab must stay open for the whole session.
  - Call `connect` with environment id, app id and the account. If sync fails with no detail, the Studio session expired: reload Studio in a fresh tab, then connect again.
- **Dataverse:** use the Dataverse plugin and MCP for small reads and writes and `scripts/deploy_schema.py` for schema (see `dataverse`).
- **Copilot Studio:** check status, sign in through the bridge (the browser prompt is the user's click), list and select the environment the user named, then load the newly available tools (`manage_agents`, `discover_resources`, the skill reader) before authoring. Read the bridge's own authoring guidance before composing a definition.
- **Connections:** the bridge can create connections: prepare a plan (it writes nothing), show the user the connector, environment and account, and only after a clear yes run the setup. Verify the connection shows Connected.

## 7. Verify

Do one harmless read through each connection you set up (list data sources, list tables, list agents). Report which work and which do not, with the exact fix for each. Then offer the next step, usually `project-starter` in a new folder.

## Things that trip people up

- A table, column or connection created after Studio opened is not visible until you save, open Studio in a fresh tab and reconnect.
- Old tabs with unsaved changes block navigation ("Leave site?"). Open a new tab instead of forcing it. A second Studio tab on the same app opens read-only until the first is closed.
- Co-authoring cannot be switched on from code: it is not in the app resource of the Power Apps API or in the downloaded app file (tested). Ask the user.
- The user does not need to rerun setup for every project. Re-check only when a tool or connection reports missing or expired.
- Never click through consent or sign-in prompts on someone's behalf; ask them.
