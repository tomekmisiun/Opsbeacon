# Architecture

## Stack
- Python 3.13 with FastAPI, Pydantic v2, SQLAlchemy 2.x, Alembic, httpx, pytest, Ruff.
- PostgreSQL 16 in Docker Compose for local and EC2 V1 deployment.
- Server-rendered Jinja2 templates and static CSS.
- Docker Compose services: `web`, `worker`, `db`.
- EC2 Ubuntu deployment with Ansible and host Nginx reverse proxy.

## Project structure
```
app/                  FastAPI application
app/api/              JSON API routes
app/core/             settings
app/db/               SQLAlchemy engine/session/base
app/models/           ORM models
app/schemas/          Pydantic request/response schemas
app/services/         monitoring, stats, URL validation
app/templates/        Jinja pages
app/static/           CSS
alembic/              database migrations
tests/                pytest suite
ansible/              EC2 provisioning and deployment
nginx/                reverse proxy config
```

## Key flows
- User opens dashboard -> FastAPI queries monitors and recent checks -> Jinja renders metrics.
- User adds monitor -> URL validation -> SQLAlchemy insert -> dashboard redirect.
- User clicks Run check -> monitoring service performs `httpx.GET` -> saves `CheckResult` -> dashboard/detail redirect.
- Worker loop -> active monitors query -> same monitoring service -> sleep configured interval.

## Boundaries & integrations
Outbound HTTP calls are isolated in `app/services/monitoring.py`. URL safety checks are isolated in `app/services/url_validation.py`. There is no authentication in V1.

## Non-goals / deliberate simplifications
No Celery, distributed queue, frontend framework, managed AWS database, Kubernetes, or Terraform in V1.
