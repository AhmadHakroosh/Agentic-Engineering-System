# DEMO-1: Create a task-management API

## Objective

Build a small production-quality HTTP API for creating, listing, and completing tasks.

## Technical constraints

- Python 3.13
- FastAPI
- SQLite persistence
- Ruff for formatting and linting
- mypy for type checking
- pytest for testing
- Build artifacts must be written to `dist/`
- The service must run locally without cloud infrastructure

## Functional requirements

1. `POST /tasks` accepts `{"title":"..."}` and creates a task with a title between 1 and 200 non-whitespace characters. It returns `201` with `id`, `title`, `completed`, and `created_at`.
2. Task IDs are server-generated UUID strings and timestamps are UTC RFC 3339 strings.
3. `GET /tasks` returns a JSON array of tasks in ascending creation order.
4. `PATCH /tasks/{id}/complete` returns the updated task and marks it complete.
5. Completing an already completed task is idempotent and returns `200`.
6. Unknown task IDs return `404` with `{"error":{"code":"task_not_found","message":"..."}}`.
7. Invalid input returns `422` with `{"error":{"code":"validation_error","message":"...","details":[]}}`.
8. `GET /health/live` returns `200` with `{"status":"ok"}` when the process can serve requests.
9. `GET /health/ready` performs a SQLite query, returning `200` with `{"status":"ready"}` or `503` with `{"status":"not_ready"}`.
10. The SQLite path is read from `TASK_API_DATABASE`, defaulting to `./data/tasks.db` for local development.
11. Tasks survive an application restart.

## Quality requirements

- Unit and API-level integration tests
- Typed application boundaries
- Atomic database operations
- Structured application logs
- No credentials committed to the repository
- Local setup and API usage documented

## Out of scope

- Authentication and authorization
- Web UI
- Task deletion or editing
- Multi-user ownership
- Container publishing
- Real production deployment

## Acceptance criteria

- All configured quality commands perform real checks and pass.
- The API behavior and failure cases are covered by automated tests.
- A fresh developer can start the service using the application README.
- The build produces a deterministic artifact under `dist/`.
- Independent correctness, security, and reliability reviews contain no blocking findings.
