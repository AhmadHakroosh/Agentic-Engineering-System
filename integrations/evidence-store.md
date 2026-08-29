# Evidence-store adapter contract

SHA-bound delivery packets and reviews cannot be committed into the Git tree they identify: that evidence commit would create a different `HEAD`. Persist them through an immutable store instead.

```ts
interface EvidenceStoreAdapter {
  put(input: EvidenceInput): Promise<EvidenceRef>;
  get(ref: EvidenceRef): Promise<EvidenceRecord>;
}

interface EvidenceInput {
  ticketId: string;
  kind: "requirements" | "design" | "delivery-packet" | "review";
  subjectSha?: string;
  schemaVersion: string;
  content: unknown;
  contentSha256: string;
  idempotencyKey: string;
}

interface EvidenceRef {
  uri: string;
  contentSha256: string;
}
```

Records must be append-only or immutable, access-controlled, auditable, and retained for at least the associated release lifetime. The adapter must reject digest mismatches and conflicting reuse of an idempotency key. PR check artifacts, immutable object storage, or an audit system can implement this contract. `.delivery/` is only an ignored local fallback for the manual walkthrough.

