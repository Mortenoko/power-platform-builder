---
name: canvas-apps
description: Lessons and working patterns for building Power Apps canvas apps through the canvas authoring MCP (sync_canvas, compile_canvas) and .pa.yaml files: layout, controls, Power Fx, Dataverse binding, publishing. Use with the canvas-apps plugin when creating or editing a canvas app.
---

# Canvas apps through the authoring MCP

Use together with the `method` skill. Edit only in the main session: sub-agents cannot use the authoring tools.

**Prerequisite: co-authoring must be enabled on the app** (Studio, Settings, General) and the app saved, with one Studio tab open. If `connect` says "Coauthoring is not enabled for this app", stop and ask the user to enable it; see the `setup` skill. Do not work around it.

## Loop

1. `sync_canvas` to a dedicated folder before editing, so you work on current YAML.
2. Make small targeted edits (or run a generator for big screens).
3. `compile_canvas`, then read the result. A "failed" result with only warnings can still have applied; check by syncing to a scratch folder.
4. Look at the result in Studio (preview or screenshot). The preview can be stale; reload it.
5. Save. **Publish only after the user gives a clear yes for that app, every time**: name the app and environment when you ask, and report what was compiled and what was not tested first. A previous yes does not cover the next publish. The authoring tools do not publish, and no code route was found, so the user publishes in Studio, where Save and Publish sit side by side; tell them which to click.

## Layout and controls

- New controls are appended at the end of their container whatever the YAML order. Moving or reparenting controls mangles them (height 1, missing labels). To add a group, create it inside **one new container with a new name**; its children keep file order. Never reuse a name under a new parent.
- Auto layout causes grey scrollbars: pin `LayoutMinHeight`/`LayoutMinWidth` to real sizes, set text padding to 0, and stretch children in vertical stacks.
- `Select(Parent)` inside galleries does not fire. Put `OnSelect` on each row control.
- Do not use `ThisItem.IsSelected` for a row fill (rows rendered black). Highlight with a global like `gblHighlightId = ThisItem.ID`.
- Modern buttons shade `BasePaletteColor`. For exact brand colours use classic buttons with explicit Fill, hover and pressed colours.
- Put colours in tokens defined once in `App` and never hard-code `RGBA(` in screens. Studio may not serialize shadow settings even though they render.
- A text label next to a conditional input needs its own `Visible`.

## Power Fx

- Avoid named formulas in `App` that depend on screen collections or later-set globals; keep that logic in the screen.
- A plain YAML scalar must not contain `: `. Put such formulas in a `|-` block (Studio may flatten them; quote when needed).
- Patch a choice column through its named option set, not `{Value: x}`, when the compiler rejects the record. Bisect a failing `OnSelect` by compiling one Patch at a time.
- `Ungroup(table, column)` takes a bare identifier.
- Wrap saves in `IfError` and show a notification either way.

## Data (Dataverse)

- Lookups use the **schema** casing (for example `cust_Customer`), plain columns the logical name. Choice columns compare through `Text(col)`.
- Native many-to-many relationships cannot be read inside `ForAll`. Use a small link table (one row per record and value) and load it into a collection.
- Load collections in the screen's `OnVisible`, not on every control. Collections hide delegation limits; keep an eye on the 500-row default.
- A source created after Studio opened is missing from Add data: save, open Studio in a fresh tab, reconnect.
- The Add data search matches display names (plural, for example "Tasks"), not the publisher prefix. A custom table can share its display name with a stock one; hover to see the logical name. Data sources added in Studio appear to the MCP only after the app is saved and co-authoring is connected.
- A choice column's option set is named after the table, for example `'Status (Tasks)'.Done`. Reading a lookup in a gallery works with `ThisItem.<Lookup>.<column>`.
- `sync_canvas` can reorder controls (a title label may come back after the gallery): that is cosmetic, check the screen.
- In an environment with another UI language the system columns have local display names; use logical names in formulas.
- When two sources share a table name, Studio suffixes the new one (`_1`). Plan the cut-over and remove the old source afterwards.

## Generators for large screens

For screens with many similar controls, write a small script that emits the YAML (containers, cards, forms) from a few parameters, apply it, compile, and iterate on the script. It makes layout changes cheap and keeps the design reproducible.

## Reporting back

After a change say what was changed, what was compiled, what was viewed in the preview, and what was **not** tested (for example save paths and role-specific views).
