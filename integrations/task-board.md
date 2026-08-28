# Task-board adapter contract

Implement this interface through MCP, an extension tool, or a separately authenticated service. Agents consume normalized output and must not receive broad account credentials.

```ts
interface TaskBoardAdapter {
  getTicket(ref: string): Promise<TicketSnapshot>;
  addDeliveryLink(ref: string, prUrl: string): Promise<void>;
  addStatus(ref: string, stage: DeliveryStage, summary: string): Promise<void>;
}

interface TicketSnapshot {
  provider: string;
  id: string;
  url: string;
  title: string;
  description: string;
  acceptanceCriteria: string[];
  labels: string[];
  updatedAt: string;
  contentDigest: string;
}
```

Reads should be default. Writes require explicit stage-scoped authorization, idempotency keys, audit logs, and no secret material in agent-visible output.

