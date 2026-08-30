# Agentic Software Delivery Starter

A language-neutral starter for a governed delivery path:

`ticket -> requirements -> architecture -> implementation -> independent review -> PR -> CI -> staging -> approved production promotion`

VS Code custom agents provide specialized reasoning. Versioned JSON contracts, repository policy, branch protection, and GitHub Actions support a fail-closed workflow around that reasoning. Agents do not approve their own work, bypass protected branches, merge pull requests, or deploy directly to production.

## What this repository gives you

- A **Delivery Orchestrator** that coordinates the workflow
- Requirements and architecture agents that work before implementation
- A builder with infrastructure, scale, microservices, and clean-code specialists
- Independent correctness, security, and reliability reviewers
- A CI investigator that diagnoses failures without silently rerunning them
- Closed JSON schemas for requirements, design, delivery, and review handoffs
- Shared engineering, security, and delivery policies
- Vendor-neutral task-board and source-control adapter contracts
- GitHub Actions for CI, PR policy, immutable release building, staging, and gated production promotion

This is a delivery framework, not an application runtime. You add your product code, toolchain, external integrations, and deployment adapter.

## Fastest safe first run

Start by taking one small feature from a written ticket to a green pull request. Do not begin with production deployment.

### 1. Create your product repository

Use this repository as the starting contents of a new Git repository, or merge the following directories into an existing codebase:

```text
.github/agents/
.github/workflows/
contracts/
docs/
integrations/
policies/
scripts/
```

Keep `.github/copilot-instructions.md`, `delivery.config.json`, and the pull-request template as well. Commit the starter to `main`, then create a feature branch for your first ticket.

### 2. Verify the starter itself

The contract and promotion checks use only Python's standard library:

```sh
python3 scripts/validate_contracts.py
python3 scripts/check_delivery_config.py
make test-unit
```

### 3. Open the repository in VS Code

Enable GitHub Copilot custom agents, open Copilot Chat, and select **Delivery Orchestrator** from the agent picker. VS Code discovers the definitions under `.github/agents/`.

If a task-board adapter is not configured yet, paste the ticket into chat as a **manual ticket snapshot**. That is the easiest way to test the workflow before connecting Jira, GitHub Issues, Linear, or another system.

### 4. Run the worked example

The [Task API example](examples/task-api/README.md) contains:

- A realistic [example ticket](examples/task-api/ticket.md)
- A copy-pasteable [requirements and design prompt](examples/task-api/prompts/01-analyze.md)
- An [implementation prompt](examples/task-api/prompts/02-build.md)
- A [delivery evidence prompt](examples/task-api/prompts/03-record-delivery.md)
- An [independent review prompt](examples/task-api/prompts/04-review.md)
- The expected files, gates, and pull-request flow

The example uses Python, FastAPI, and SQLite, but the workflow is stack-independent. Replace the ticket's technical constraints with the language, framework, storage, and deployment target appropriate to your product.

### 5. Approve decisions before implementation

The first orchestration pass should produce:

```text
.delivery/<ticket-id>/requirements.json
.delivery/<ticket-id>/design.json
```

Review these files. Resolve blocking ambiguity, security exceptions, public API changes, migrations, new paid services, and irreversible decisions before authorizing the builder.

### 6. Build and review

After approval, the builder implements the design and runs the configured commands. Commit the application changes first. The orchestrator then binds a delivery packet to that exact committed code SHA:

```text
.delivery/<ticket-id>/delivery-packet.json
```

The Independent Reviewer then runs separate correctness, security, and reliability reviews and returns a review contract to the orchestrator for persistence:

```text
.delivery/<ticket-id>/review.json
```

`.delivery/` is ignored by Git because committing SHA-bound evidence would change the SHA it describes. For the manual walkthrough it is local working evidence; a real source-control adapter should persist it as a PR check artifact, PR comment, or external append-only evidence record.

Any material code change makes the existing packet and review stale because their recorded SHA no longer matches the committed code. Fixes must be committed, checked, recorded, and reviewed again.

### 7. Open a pull request

Until the source-control adapter is implemented, create the branch and pull request manually. Fill in `.github/pull_request_template.md` and paste or securely attach the requirements, design, delivery packet, and review references. Do not commit `.delivery/` merely to obtain a link.

Protect `main` and require these checks:

- `contracts`
- `project-checks`
- `metadata`

See [Repository operations](docs/operations.md) for the required GitHub ruleset and environment configuration.

## Adapting the starter to your stack

Update `delivery.config.json` so every command invokes a deterministic check that already works locally:

```json
{
  "commands": {
    "formatCheck": "your format check",
    "lint": "your linter",
    "typecheck": "your type checker",
    "unitTest": "your unit tests",
    "integrationTest": "your integration tests",
    "build": "your build command",
    "securityScan": "your approved security scanners"
  }
}
```

The starter `Makefile` intentionally contains placeholders for application type checking, integration testing, and security scanning. Replace them before treating CI as a real quality gate. Ensure the build places its release artifact under the configured `release.artifactPath`—`dist/` by default. The release workflow reads this setting and rejects paths outside the repository.

## Connecting external systems

No vendor is hard-coded. Implement the narrow contracts in `integrations/` through an MCP server, a trusted extension, or a separately authenticated service:

- `integrations/task-board.md`: read tickets and write limited delivery status
- `integrations/source-control.md`: create branches and pull requests and read checks
- `integrations/evidence-store.md`: persist immutable SHA-bound delivery and review evidence

Start with read access. Add stage-scoped write access only when needed. The source-control adapter must not approve, merge, alter branch protection, create releases, or deploy.

## Enabling deployment

The checked-in workflows prove the immutable promotion mechanics but are deliberately inert at the cloud boundary. Before real deployment:

1. Replace the marked staging and production adapter steps.
2. Use short-lived OIDC identity rather than stored cloud credentials.
3. Make staging verification deterministic and fail closed.
4. Configure a protected `production` GitHub environment with human reviewers and self-review prevention.
5. Promote the exact artifact digest verified in staging; never rebuild for production.

See [Repository operations](docs/operations.md) and [Delivery policy](policies/delivery.md).

## Repository map

- `.github/agents/`: orchestrator, builders, specialists, reviewers, and CI investigator
- `.github/copilot-instructions.md`: always-on engineering constraints
- `.github/workflows/`: CI, PR policy, release build, and gated promotion
- `contracts/`: machine-readable handoff schemas and schema examples
- `examples/`: worked tickets and orchestration prompts
- `integrations/`: task-board, source-control, and evidence-store interfaces
- `policies/`: engineering, security, and delivery rules
- `scripts/`: dependency-free contract and promotion checks
- `docs/`: workflow, threat model, and repository operations

## Further reading

- [Production autonomy roadmap](ROADMAP.md)
- [Governed delivery workflow](docs/workflow.md)
- [Repository operations](docs/operations.md)
- [Threat model](docs/threat-model.md)
- [VS Code custom agents](https://code.visualstudio.com/docs/agent-customization/custom-agents)
- [VS Code subagents](https://code.visualstudio.com/docs/agents/run/subagents)
