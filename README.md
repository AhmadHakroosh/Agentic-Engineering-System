# Agentic Software Factory Starter

A language-neutral starter for a controlled delivery path:

`ticket -> analysis -> architecture -> implementation -> independent review -> PR -> CI -> staging -> approved production promotion`

VS Code custom agents provide specialized reasoning. Versioned JSON contracts, repository policy, and GitHub Actions provide deterministic enforcement. Agents never bypass branch protection, approve their own work, or deploy to production.

## Start here

1. Open this repository in VS Code and enable GitHub Copilot custom agents.
2. Configure a task adapter and source-control adapter from `integrations/README.md`.
3. Select **Delivery Orchestrator** and provide a ticket reference.
4. Review the generated delivery packet before allowing implementation.
5. Configure GitHub branch protection and the `production` environment as described in `docs/operations.md`.

The repository intentionally contains no application runtime. Add your product code and replace the `make`-based commands in `delivery.config.json` with your project's deterministic commands.

## Repository map

- `.github/agents/`: orchestrator, builders, specialists, reviewers, and CI investigator
- `.github/copilot-instructions.md`: always-on engineering constraints
- `contracts/`: machine-readable handoff schemas and examples
- `policies/`: human-readable engineering, review, and release rules
- `integrations/`: task-board and source-control interfaces
- `scripts/`: dependency-free contract and promotion checks
- `.github/workflows/`: CI, PR policy, release build, and gated promotion
- `docs/`: workflow, threat model, and repository setup

## Local verification

```sh
python3 scripts/validate_contracts.py
python3 scripts/check_delivery_config.py
```

See `docs/workflow.md` for the lifecycle and `docs/operations.md` for required GitHub settings.

