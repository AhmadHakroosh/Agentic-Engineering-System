# Source-control adapter contract

```ts
interface SourceControlAdapter {
  createBranch(baseSha: string, name: string): Promise<BranchRef>;
  openDraftPullRequest(input: PullRequestInput): Promise<PullRequestRef>;
  updatePullRequest(id: string, expectedHeadSha: string, body: string): Promise<void>;
  getChecks(headSha: string): Promise<CheckResult[]>;
}
```

The adapter must use least privilege, require an exact base/head SHA, reject protected-branch writes, escape untrusted ticket content, be idempotent, and preserve audit logs. It must not approve, merge, alter branch protection, create releases, or deploy. GitHub Apps with short-lived installation tokens are preferred over personal access tokens.

