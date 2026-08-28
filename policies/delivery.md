# Delivery policy

## Gates

1. Requirements are normalized and blocking ambiguity is resolved.
2. Design covers risk, testing, rollout, rollback, and required human decisions.
3. Builder checks pass and a delivery packet identifies the exact head commit.
4. Independent correctness, security, and reliability reviews cover that same commit.
5. Protected CI passes on the PR; review becomes stale after material changes.
6. Merge occurs through branch protection, never by an agent bypass.
7. The merged commit is built exactly once. Its SHA-256 digest is recorded.
8. That artifact is deployed and verified in staging.
9. Production promotion requires the protected `production` environment and promotes the identical digest without rebuilding.

Production must be fail-closed: missing approval, mismatched commit, missing digest, failed staging evidence, or concurrent promotion stops the workflow.

