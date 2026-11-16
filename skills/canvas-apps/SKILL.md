---
name: canvas-apps
description: Lessons and working patterns for building Power Apps canvas apps through the canvas authoring MCP (sync_canvas, compile_canvas) and .pa.yaml files: layout, controls, Power Fx, Dataverse binding, publishing. Use with the canvas-apps plugin when creating or editing a canvas app.
---

# Canvas apps through the authoring MCP

Use together with the `method` skill. Edit only in the main session: sub-agents cannot use the authoring tools.

## Loop

1. `sync_canvas` to a dedicated folder before editing, so you work on current YAML.
2. Make small targeted edits (or run a generator for big screens).
3. `compile_canvas`, then read the result. A "failed" result with only warnings can still have applied; check by syncing to a scratch folder.
4. Look at the result in Studio (preview or screenshot). The preview can be stale; reload it.
5. Save. **Publish only when the user says so.** Studio shows Save and Publish side by side; check before clicking.

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
- When two sources share a table name, Studio suffixes the new one (`_1`). Plan the cut-over and remove the old source afterwards.

## Generators for large screens

For screens with many similar controls, write a small script that emits the YAML (containers, cards, forms) from a few parameters, apply it, compile, and iterate on the script. It makes layout changes cheap and keeps the design reproducible.

## Reporting back

After a change say what was changed, what was compiled, what was viewed in the preview, and what was **not** tested (for example save paths and role-specific views).
