# Roadmap

## Phase 0 - OpsBeacon V1
Goal: complete public demo uptime monitor deployable to one Ubuntu EC2 host.
Exit criteria:
- [x] `docker compose up --build` serves the dashboard on `http://localhost:8000`.
- [x] API supports monitor CRUD, manual checks, history, `/health`, and `/version`.
- [x] Worker periodically checks active monitors.
- [x] `pytest`, `ruff check .`, and `docker compose config` pass.
- [x] Ansible playbook passes syntax validation.
- [x] README documents local use, EC2 deployment, security, limitations, and V2 path.

## Phase 1 - V2 Cloud Migration
Goal: move from single-host Compose to managed AWS infrastructure.
Exit criteria:
- [ ] Terraform provisions VPC, ECS Fargate, ALB, RDS, ECR, CloudWatch, Route53, and ACM.
- [ ] CI can build and publish images safely.
- [ ] Deployment uses managed secrets and no hardcoded credentials.
