---
name: flows
description: Method and lessons for building Power Automate cloud flows with Claude: use Microsoft's power-automate plugin (FlowAgent MCP) to create, edit, run and debug, with solution-first, connection references and approval gates on top. Use when a flow must be created, changed, deployed, turned on, run or debugged.
---

# Power Automate flows

Use together with the `method` skill. **Do the authoring with Microsoft's `power-automate` plugin** (the FlowAgent MCP and its skills: `build-flow`, `create-flow`, `manage-flows`, `debug-flow`, `diagnose-flow`). It is installed as a dependency of this plugin; it needs Node.js 18 or newer and `az login`. This skill adds the method and lessons on top and does not duplicate it.

## What this plugin adds

- **Solution-first.** Create the flow inside your solution (pass the solution to the create call), never loose in "My flows". Afterwards export and unpack the solution so the repo holds the definition.
- **Connection references and environment variables** for sites, lists and ids, so the solution moves between environments. Never hard-code ids. Check the connection reference is **in the solution**: a reference created outside it (for example through the Copilot Studio bridge) lands with the default publisher prefix and must be added to the solution.
- **Approval gates.** Turning a flow on (`publish_flow`) and running it (`run_flow`) need a clear yes from the user. Before either, say who the flow sends to and what it writes; a flow that notifies people needs explicit approval every time. Flows are created switched off.
- **Verify, don't assume.** After a run, read every action's status, not only the run status. Say what was tested and what was not.
- **Telemetry.** The Microsoft plugin sends pseudonymous usage metadata (tool names, outcome, environment, tenant and organisation ids) by default and can be switched off with `/power-automate:telemetry off`. Tell the user at setup so they can decide.

## Fallback without the plugin

If Node or the plugin is unavailable, a cloud flow is a Dataverse `workflow` row (category 5): POST it through the Web API with `clientdata` (a JSON string of `{properties: {connectionReferences, definition}, schemaVersion}`) and the `MSCRM.SolutionUniqueName` header. A connection reference entry is `{runtimeSource: "embedded", connection: {connectionReferenceLogicalName}, api: {name}}`. Turn on with `statecode 1`, `statuscode 2` after approval. Run a manual trigger with `POST .../flows/<id>/triggers/manual/run?api-version=2016-11-01` on `api.flow.microsoft.com` and read `.../runs` and `.../runs/<id>/actions`. Generate the JSON from a builder script kept in the repo.

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
