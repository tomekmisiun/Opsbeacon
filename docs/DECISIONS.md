# Decision log

## D-005 (2026-08-21) HTTP Failure Status Semantics
**Decision**: Treat monitor responses with HTTP status `<400` as UP and `>=400` as DOWN. **Why**: uptime should reflect user-visible HTTP failures, not only network transport failures. **Instead of**: recording every completed HTTP response as UP. **Consequences**: 4xx/5xx responses are stored with their status code and counted as downtime.

## D-004 (2026-08-21) Generic Attribution Guard
**Decision**: Block attribution trailers and generated/written-by phrasing generically in hooks and CI. **Why**: the guardrails should enforce the project rule without naming specific tools in project artifacts. **Instead of**: maintaining a tool-name denylist. **Consequences**: `Co-Authored-By` trailers are not allowed in this repo.

## D-003 (2026-08-19) FastAPI Compatibility Pin
**Decision**: Pin FastAPI to `>=0.115,<0.116` and httpx to `>=0.27,<0.28`. **Why**: the latest resolved FastAPI/Starlette/httpx combination hung in local test transport on Python 3.14, while V1 targets a stable Python 3.13 deployment. **Instead of**: chasing future transport API behavior during V1. **Consequences**: dependency upgrades should be a separate task with test-client/runtime verification.

## D-002 (2026-08-19) Simple Worker Loop
**Decision**: Use a dedicated Python worker container with a sleep loop for periodic checks. **Why**: V1 needs one reliable background process without queue complexity. **Instead of**: Celery or a scheduler embedded in the web process. **Consequences**: higher-throughput scheduling can replace only `app/worker.py` later.

## D-001 (2026-08-19) V1 Stack
**Decision**: Build OpsBeacon V1 with FastAPI, SQLAlchemy 2.x, Alembic, PostgreSQL, Jinja2, Docker Compose, Ansible, and Nginx. **Why**: it demonstrates backend and DevOps fundamentals without frontend or cloud-service noise. **Instead of**: React/Next.js, Celery, Terraform, ECS, or RDS in V1. **Consequences**: V2 can migrate infrastructure while keeping the app boundary stable.
