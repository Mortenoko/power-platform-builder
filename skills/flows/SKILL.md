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
