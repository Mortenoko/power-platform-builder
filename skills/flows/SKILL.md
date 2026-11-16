---
name: flows
description: Lessons and patterns for creating and deploying Power Automate cloud flows as code (Dataverse workflow records, solution-aware, connection references, environment variables) with Claude. Use when a flow must be created, changed, deployed or debugged.
---

# Power Automate flows as code

Use together with the `method` skill and, for the JSON structure, a flow-authoring skill if one is installed.

## Principles

- Flows are Dataverse `workflow` records (category 5). Create them through the Web API with the solution header (`MSCRM.SolutionUniqueName`), not by packing hand-written solution folders.
- Generate the flow JSON from a **builder script** and keep the builder in the repo; the JSON is a build output.
- Use **connection references** and **environment variables** for sites, lists and ids so the same solution moves between environments. Never hard-code ids.
- Activate with `statecode 1 / statuscode 2` only after the user approves; flows import switched off.
- Before turning a flow on, check who it sends to and what it writes. Flows that notify people need explicit approval.

## Everything from code

1. **Connection:** create it through the Copilot Studio bridge (prepare a plan, get the user's yes, run setup). It returns a connection reference with the default publisher prefix, **not in your solution**: add it with `AddSolutionComponent` (look up the component type code).
2. **Create:** POST `workflows` with `category 5`, `type 1`, `primaryentity none`, `clientdata` as a JSON string and the solution header. `clientdata` is `{properties: {connectionReferences, definition}, schemaVersion}`; a connection reference entry is `{runtimeSource: "embedded", connection: {connectionReferenceLogicalName}, api: {name}}`, and actions refer to it by the connector name (for Dataverse an `OpenApiConnection` action such as `ListRecords`).
3. **Edit:** PATCH `clientdata` on the row (the flow is off while you edit).
4. **Turn on:** PATCH `statecode 1`, `statuscode 2`, after the user approves.
5. **Run and inspect:** for a manual trigger, POST `.../flows/<id>/triggers/manual/run?api-version=2016-11-01` on `api.flow.microsoft.com` (token for `https://service.flow.microsoft.com/`), then read `.../runs` and `.../runs/<id>/actions`. Check every action, not just the run status.

## Lessons

- Update SharePoint items with an HTTP/REST MERGE if the `PatchItem` action fails on missing item or title.
- A SharePoint trigger ignores items created before the flow was switched on. Test with a fresh item.
- In a JSON body write `@@odata.id` to send a literal `@odata.id`.
- Dataverse triggers use the webhook trigger (message 3 modified, 4 added or modified, scope organization) with a `filterexpression`. Lookups arrive as `_column_value`; bind child rows with `Column@odata.bind: entityset(<id>)`.
- A flow that updates the row it triggers on must not match its own filter again: set a different status first.
- Group and membership actions take a UPN, not an id.
- Keep a step log table (one row per step with status) so failures are visible to users, and add a retry path.
- A Power Automate connector cannot call a Copilot Studio agent built as a harness/workflow agent. If a flow needs AI text, use an AI prompt or HTTP action, or run the work from Copilot Studio.

## Test and verify

1. Run once end to end with a new record. Read the run history, not just the final status.
2. Test the unchanged, add and remove paths when a flow syncs data.
3. Export the solution afterwards so the repo holds the final definition.
