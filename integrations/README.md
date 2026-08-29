# Integration setup

No vendor is hard-coded. Bind the task-board, source-control, and evidence-store contracts using an MCP server, trusted extension, or separately authenticated service and expose only the narrow methods each agent needs.

For an MVP, GitHub Issues plus a GitHub App can implement the task-board and source-control contracts. Jira, Linear, or another board can implement the task side without changing agent prompts. Keep credentials outside the repository and return normalized snapshots with a content digest so the delivery packet can detect ticket drift.

Use `evidence-store.md` for SHA-bound delivery packets and reviews. Do not commit that evidence into the source tree it identifies.
