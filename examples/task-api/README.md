# Worked example: Task API

This walkthrough starts with an otherwise empty product repository and builds a small task-management API. Its purpose is to exercise the delivery system—not to prescribe Python or FastAPI for every project.

## Outcome

At the end of the first exercise you should have:

- Approved requirements and design contracts
- A working application with automated tests
- A delivery packet bound to an exact commit
- Independent correctness, security, and reliability review evidence
- A pull request with the required CI checks

Stop there for the first run. The deployment workflows require target-specific adapters before they can deploy anything real.

## Prerequisites

- VS Code with GitHub Copilot custom agents enabled
- Python 3.13 available locally for this particular example

You do not need Jira or a source-control adapter. The first prompt supplies a manual ticket snapshot, and you can create the pull request manually.

Initialize the repository before asking agents to build anything, so later evidence has a real base SHA:

```sh
git init -b main
git add .
git commit -m "Initialize agentic delivery starter"
git switch -c demo/DEMO-1-task-api
```

If the starter is already committed, create only the feature branch.

## 1. Analyze the ticket

Open Copilot Chat, select **Delivery Orchestrator**, and submit the contents of [`prompts/01-analyze.md`](prompts/01-analyze.md) and [`ticket.md`](ticket.md) together in one message.

The orchestrator should delegate requirements and architecture analysis and then stop. It should not implement code yet.

Expected outputs:

```text
.delivery/DEMO-1/requirements.json
.delivery/DEMO-1/design.json
```

Validate the generated instances with:

```sh
python3 scripts/validate_instance.py contracts/schemas/requirements.schema.json .delivery/DEMO-1/requirements.json
python3 scripts/validate_instance.py contracts/schemas/design.schema.json .delivery/DEMO-1/design.json
```

Review database evolution, error contracts, dependency management, artifact construction, rollout, rollback, and anything the agents classified as requiring human approval.

## 2. Approve and build

Resolve blocking questions in the ticket or contracts. When the design is acceptable, submit [`prompts/02-build.md`](prompts/02-build.md) to the **Delivery Orchestrator**.

The Builder Coordinator should implement the application and configure the real project commands. For this example, those commands should cover at least:

- Ruff formatting and linting
- mypy type checking
- pytest unit and API-level integration tests
- A deterministic build under `dist/`
- The repository-approved dependency and static security checks

The builder should stop after the application and its checks are ready. Inspect the diff, then create the code commit that later evidence will identify:

```sh
git add .
git commit -m "Build DEMO-1 task-management API"
```

Do not add `.delivery/`; it is intentionally ignored because committing SHA-bound evidence would change the SHA it records.

## 3. Record delivery evidence

Submit [`prompts/03-record-delivery.md`](prompts/03-record-delivery.md) to the **Delivery Orchestrator**. It should run checks against the committed code and create:

```text
.delivery/DEMO-1/delivery-packet.json
```

Validate it with:

```sh
python3 scripts/validate_instance.py contracts/schemas/delivery-packet.schema.json .delivery/DEMO-1/delivery-packet.json
```

Do not accept `echo` placeholders as successful project checks. Each command in `delivery.config.json` must perform the named check and return a failure status when the check fails.

## 4. Review independently

Use the orchestrator's **Review delivery packet** handoff and submit [`prompts/04-review.md`](prompts/04-review.md). The read-only Independent Reviewer returns the contract; the orchestrator persists it.

Expected additional output:

```text
.delivery/DEMO-1/review.json
```

Validate it with:

```sh
python3 scripts/validate_instance.py contracts/schemas/review.schema.json .delivery/DEMO-1/review.json
```

The review must cover the committed code at the current `HEAD`. If the builder changes code to address findings, create a new code commit, regenerate the delivery packet, and repeat independent review.

## 5. Open the pull request

Push the feature branch. Until a source-control adapter exists, open the pull request manually and fill in `.github/pull_request_template.md`:

```sh
git push -u origin demo/DEMO-1-task-api
```

For this manual walkthrough, paste the evidence into a PR comment or attach it through your approved evidence store. Do not commit `.delivery/`. In a real integration, the source-control adapter should publish the evidence as a check artifact, PR comment, or append-only external record.

The pull request should not be mergeable until:

- `contracts` passes
- `project-checks` passes
- `metadata` passes
- Blocking review findings are resolved
- The required human approval is present

## 6. Reuse the workflow for your own product

Copy this example and replace the ticket. Good first tickets are small, observable, reversible, and testable—for example:

- Add an endpoint to an existing service
- Create a small CLI
- Add a background job with bounded retries
- Build a static frontend backed by a mock API
- Add an infrastructure module without applying it

Avoid starting with a destructive database migration, a production credential change, or a multi-service rewrite. Establish that the requirements, build, review, and CI loop works first.
