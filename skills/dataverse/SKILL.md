---
name: dataverse
description: Working rules for Dataverse in a Power Platform build: schema as code with the Python SDK, solution-first, publisher prefix, choices, lookups, link tables, security roles, data migration and solution export. Use when creating tables or columns, seeding or migrating data, or exporting a solution.
---

# Dataverse

Use together with the `method` skill and the `dataverse` plugin skills (connect, metadata, data, query, solution).

## Rules

- Confirm the environment (`pac org who`) and the **solution and publisher prefix** before creating anything. The prefix is permanent. Create components only inside the solution.
- Use the **Python SDK** for tables, columns and bulk data; use the Dataverse MCP for small reads and writes; use the raw Web API only where the SDK cannot (forms, views, global option sets, `$apply`, unbound actions, memo columns).
- Keep the **schema as code** in one file, and make the deploy script idempotent with a dry-run default, an `--apply` switch and a verify step (check existence before each create).
- Start from the plugin's `scripts/deploy_schema.py` (with `scripts/example_schema.json` as the format): set `DATAVERSE_URL`, copy and edit the schema file into the project, run it without flags for a dry run, then with `--apply`. Re-running changes nothing. It creates the publisher and solution if missing, so confirm the prefix with the user first.
- The raw Web API works well for metadata with a bearer token from the Azure CLI. Send `MSCRM.SolutionUniqueName: <Solution>` on every metadata create so tables, columns and relationships land in the solution. URL-encode spaces in `$filter`.
- Creating a lookup: POST `RelationshipDefinitions` with `"@odata.type": "Microsoft.Dynamics.CRM.OneToManyRelationshipMetadata"` (without it the payload is rejected on `ReferencedEntity`). Create the tables first and pause a few seconds.
- Adding an existing component to the solution: `AddSolutionComponent`. Component type codes for newer components (for example connection references) differ per environment; look them up in `solutioncomponentdefinitions` instead of hard-coding.
- Do not name a plain column with an `Id` suffix; it collides with a lookup navigation property later.
- Choice values are integers; keep a table of label to value in the schema file.
- Lookup `@odata.bind` keys use the navigation property name with exact casing and the entity set name (pluralisation is not always `+s`).
- Many-to-many that a canvas app must read in bulk: use a **link table** (lookup to each side), not a native relationship.
- After creating a lookup, wait a few seconds before inserting data.

## Migration

Import in dependency order with upserts on an alternate key (the source id), keep the source id on every migrated row, resolve lookups from maps built after each level, and compare counts at the end.

## Security

Create security roles as code, assign them by script, and test with a real user in the lowest role, not only as an admin.

## Export after every publish

```bash
pac solution export --name <Solution> --path solution/zip/<Solution>_unmanaged.zip --managed false --overwrite
pac solution unpack --zipfile solution/zip/<Solution>_unmanaged.zip --folder solution/src --packagetype Unmanaged --allowDelete true --allowWrite true
```

This is what keeps the repo and the environment in step.
