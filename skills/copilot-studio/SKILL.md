---
name: copilot-studio
description: Lessons and patterns for building Copilot Studio agents and workflows with Claude through the Copilot Studio MCP bridge: connecting, designing agents, workflows that call agents, files and knowledge, and testing. Use when building or debugging a Copilot Studio agent or workflow, or deciding between an agent, a flow and an AI prompt.
---

# Copilot Studio agents and workflows

Use together with the `method` skill and the Copilot Studio plugin skills (authoring, validation, testing).

## Connect first

Check status, sign in if needed, pick the environment (never choose production implicitly), and refresh the tool list before authoring. Keep the user's original request through the sign-in steps.

## Choosing the building block

| Need | Use |
|---|---|
| Deterministic steps, scheduled or event-driven | Power Automate flow |
| One prompt over known input, no tools | AI prompt in a flow |
| Reasoning over documents and tools, several steps | Agent |
| A repeatable process that calls an agent with inputs and collects the result | Copilot Studio workflow |

## Lessons

- Keep instructions short and concrete: purpose, inputs, output structure, what to never do. Test each instruction change with a fixed set of prompts.
- A workflow that calls an agent is the way to run an agent from a button or a record; a normal flow connector cannot call that kind of agent.
- An agent that writes files can be **inconsistent**: in testing it produced the files roughly two runs in three. Design for it: check that the expected output exists, retry once, and surface a clear failure instead of silently continuing.
- Put the facts the agent needs in structured input (ids, fields) and let it read documents for the rest. Prefer reading approved or final documents first.
- Generated content that people will use needs a **review state** (draft, in review, published). Never publish unreviewed AI output.
- Anonymisation is an instruction **and** a check: strip names, logos and identifying figures, then verify the output.
- Publish the agent only when the user approves. Drafts can be tested without publishing.

## Test

Use evaluation sets or point tests with a fixed prompt list, run before and after each change, and keep the transcripts. Report which prompts passed and which were not tried.
