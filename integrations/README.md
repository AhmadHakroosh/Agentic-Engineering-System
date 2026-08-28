# Integration setup

No vendor is hard-coded. Bind the task-board and source-control contracts using an MCP server or trusted extension and expose only the narrow methods each agent needs.

For an MVP, GitHub Issues plus a GitHub App can implement both contracts. Jira, Linear, or another board can implement the task side without changing agent prompts. Keep credentials outside the repository and return normalized snapshots with a content digest so the delivery packet can detect ticket drift.

