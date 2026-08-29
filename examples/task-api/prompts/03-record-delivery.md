The approved DEMO-1 implementation is now committed at the current `HEAD`.

Confirm the worktree has no application changes, run every configured check against this commit, and create:

- `.delivery/DEMO-1/delivery-packet.json`

Bind `headSha` to the exact full current commit SHA and `baseSha` to the starter commit from which the feature branch was created. Do not add `.delivery/` to Git. Run `scripts/validate_instance.py` with `contracts/schemas/delivery-packet.schema.json` and report the result. Do not approve, merge, or deploy.

