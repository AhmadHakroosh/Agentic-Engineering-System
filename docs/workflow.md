# Governed delivery workflow

| Stage | Owner | Durable output | Exit gate |
|---|---|---|---|
| Intake | Orchestrator | ticket snapshot + digest | Ticket accessible and in scope |
| Requirements | Requirements Analyst | requirements contract | Blocking ambiguity resolved |
| Design | Solution Architect | design contract | Risk and human decisions accepted |
| Build | Builder Coordinator | code, tests, delivery packet | Configured checks pass |
| Review | Independent Reviewer | review contract | No blocking findings on current SHA |
| PR | Source-control adapter | draft/ready PR | Branch protection and CI pass |
| Release | GitHub Actions | artifact + SHA-256 digest | Built once from merged SHA |
| Staging | Deployment adapter | promotion evidence | Deterministic verification passes |
| Production | Human + protected environment | deployment record | Exact staged digest approved |

Any code change after review invalidates review evidence because `reviewedHeadSha` no longer matches. Any ticket change after intake should be compared using its content digest and sent back through requirements analysis if material.

Agent recommendations are advisory. Schemas, CI, branch rules, exact SHAs/digests, environment protection, and human approvals are enforcement boundaries.

