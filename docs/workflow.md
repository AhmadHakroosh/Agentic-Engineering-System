# Governed delivery workflow

| Stage | Owner | Durable output | Exit gate |
|---|---|---|---|
| Intake | Orchestrator | ticket snapshot + digest | Ticket accessible and in scope |
| Requirements | Requirements Analyst | requirements contract | Blocking ambiguity resolved |
| Design | Solution Architect | design contract | Risk and human decisions accepted |
| Build | Builder Coordinator | committed code and tests | Configured checks pass |
| Evidence | Orchestrator | delivery packet outside reviewed tree | Packet matches committed code SHA |
| Review | Independent Reviewer + Orchestrator | review contract outside reviewed tree | No blocking findings on committed code SHA |
| PR | Source-control adapter | draft/ready PR | Branch protection and CI pass |
| Release | GitHub Actions | artifact + SHA-256 digest | Built once from merged SHA |
| Staging | Deployment adapter | promotion evidence | Deterministic verification passes |
| Production | Human + protected environment | deployment record | Exact staged digest approved |

SHA-bound delivery and review evidence must not be committed into the tree it identifies because that evidence commit would change the SHA. Persist it as a PR check artifact, PR comment, or append-only external record. `.delivery/` is an ignored local fallback for the manual walkthrough.

Any code change after evidence or review invalidates those records because their SHA no longer matches. Commit the fix, regenerate the delivery packet, and review again. Any ticket change after intake should be compared using its content digest and sent back through requirements analysis if material.

Agent recommendations are advisory. Schemas, CI, branch rules, exact SHAs/digests, environment protection, and human approvals are enforcement boundaries.
