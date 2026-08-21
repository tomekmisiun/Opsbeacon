# Specification

## Problem
Recruiters and reviewers need to see a deployed DevOps portfolio project that is more realistic than a static page. OpsBeacon demonstrates a small production-style monitoring system: HTTP checks, persistence, background work, containerization, CI, and server provisioning.

## Users
Primary users are recruiters and hiring managers evaluating the portfolio. Secondary users are the project owner during local development and deployment practice.

## Core features (MVP)
1. Dashboard lists monitored services with status, uptime, response time, HTTP status, and last check. Works means `/` renders seeded monitors and their latest metrics.
2. Public monitor management API supports create, list, detail, delete, manual check, and history. Works means the documented `/api/v1/monitors` endpoints return proper status codes and JSON.
3. Manual and periodic HTTP checks record UP/DOWN, status code, latency, error, and timestamp. Works means mocked service tests cover success, timeout/error, and uptime calculation.
4. Demo mode seeds stable public HTTPS monitors idempotently. Works means `make seed` can be run repeatedly without duplicates.
5. DevOps runtime runs via Docker Compose with web, worker, and PostgreSQL. Works means `docker compose up --build` serves the app on `http://localhost:8000`.
6. EC2 provisioning path uses Ansible and Nginx. Works means the playbook passes syntax validation and configures Docker, app files, Compose, and reverse proxy.

## Later (post-MVP)
Terraform, AWS VPC, ECR, ECS Fargate, ALB, RDS PostgreSQL, CloudWatch, Route53, ACM, authentication, teams, alerts, and HTTPS automation.

## Out of scope
React/Next.js, Celery, Kubernetes, ECS/EKS, Terraform, RDS, and automatic AWS resource creation are out of scope for V1 to keep the project deployable and understandable.

## Constraints
Python 3.13, FastAPI, SQLAlchemy 2.x, Alembic, PostgreSQL, Pydantic v2, pytest, httpx, Docker, Docker Compose, Ansible, Nginx, GitHub Actions, and simple server-rendered HTML/CSS.
