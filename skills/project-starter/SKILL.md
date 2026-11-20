---
name: project-starter
description: Start a new Power Platform project with the standard structure: CLAUDE.md with environment and rules, README, architecture doc, backlog and folder layout. Use when someone begins a new app, flow or agent project, or asks how to organise the repo.
---

# Project starter

Ask the user for: project name, tenant and account, environment name and URL, solution name, publisher prefix, and where the backlog lives. Then create:

```
<project>/
  CLAUDE.md            from templates/CLAUDE.md.template, filled in
  .claude/settings.json  from templates/settings.json.template (read-only allowlist)
  README.md            data model, URLs, runbook (keep it true)
  BACKLOG.md           snapshot, the live list is the source of truth
  app/                 canvas source (.pa.yaml)
  scripts/             schema as code, deploy, seed, export
  flow/                flow builders and generated JSON
  docs/architecture.md diagrams (see templates/architecture.md.template)
  solution/            exported solution (zip + unpacked)
```

The read-only allowlist (`.claude/settings.json`) stops Claude asking for approval on harmless checks: `pac org who`, `pac auth list`, `pac solution list`, `az account show`, `git status`, the setup status script and read-only list/describe MCP tools. It allows nothing that changes data, signs in, publishes or deletes, so every write still asks. Copy it into the project (ask first), and tell the user Claude Code only applies project settings after they accept the one-time trust dialog for the folder.

Rules for the starter:
- Put environment, account and approval rules at the top of `CLAUDE.md`; this is what protects the next session.
- Do not copy secrets, tokens or personal data into any file.
- Keep a "lessons learned" section in `CLAUDE.md` and add to it whenever something surprised you.
- Commit the first working state before large changes.

Templates: `templates/CLAUDE.md.template`, `templates/architecture.md.template` and `templates/settings.json.template` in this plugin.
