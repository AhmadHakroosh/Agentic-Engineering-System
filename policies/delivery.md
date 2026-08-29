# Delivery policy

## Gates

1. Requirements are normalized and blocking ambiguity is resolved.
2. Design covers risk, testing, rollout, rollback, and required human decisions.
3. Builder checks pass and the code is committed.
4. An immutable delivery packet outside the reviewed Git tree identifies that exact code commit.
5. Independent correctness, security, and reliability reviews cover that same commit and are persisted outside the reviewed tree.
6. Protected CI passes on the PR; evidence and review become stale after material changes.
7. Merge occurs through branch protection, never by an agent bypass.
8. The merged commit is built exactly once after post-merge CI succeeds. Its SHA-256 digest is recorded.
9. That artifact is deployed and verified in staging.
10. Production promotion requires the protected `production` environment and promotes the identical digest without rebuilding.

Production must be fail-closed: missing approval, mismatched commit, missing digest, failed staging evidence, or concurrent promotion stops the workflow.
