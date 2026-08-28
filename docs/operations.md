# Repository operations

## Required GitHub configuration

Protect `main` and require pull requests, at least one human approval, dismissal of stale approvals, resolution of conversations, linear history if desired, and these checks: `contracts`, `project-checks`, and `metadata`. Prevent force pushes and branch deletion. Do not grant agents bypass rights.

Create environments:

- `staging`: restrict to `main`; configure only staging identity and variables.
- `production`: restrict to `main`, add required human reviewers, prevent self-review, and configure production identity only here.

Use OIDC/short-lived federation in deployment adapters. Environment secrets are not available until protection rules pass. Restrict Actions to approved actions and review every pinned SHA update.

## Adopting the workflows

Replace configured `make` commands with commands that already work locally. Implement the two placeholder deployment steps with reviewed scripts or reusable workflows. Both must accept an artifact path, expected digest, and target environment; neither may build source. Make verification return nonzero on failure and make production deployment perform or trigger rollback.

The checked-in workflows are deliberately inert at the cloud boundary: they demonstrate and enforce promotion mechanics but cannot deploy until an operator supplies a target-specific adapter.

