Delegate an independent review of DEMO-1 at the current committed `HEAD`. The reviewer must not modify code or claim to write files.

Have the Independent Reviewer inspect the approved requirements and design, the base-to-head diff, callers, tests, build configuration, runtime behavior, and delivery packet. Require independent correctness, security, and reliability review passes.

Persist the returned consolidated contract as:

- `.delivery/DEMO-1/review.json`

Run `scripts/validate_instance.py` with `contracts/schemas/review.schema.json`. Cite exact evidence for every finding, distinguish blocking findings from recommendations, and verify that `reviewedHeadSha` equals the current full commit SHA. Do not add `.delivery/` to Git.

