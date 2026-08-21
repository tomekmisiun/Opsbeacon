# Tasks

<!-- The working board. Agents read this at session start and update it as work happens. -->
<!-- A task = ID, title, phase ref, and VERIFY line (how we know it's done). No VERIFY = not a task yet. -->
<!-- Keep Now at exactly 0-1 tasks. Multi-tasking is how plans die. -->
<!-- Branch naming maps to tasks: <type>/T-012-short-slug (see AGENTS.md → Git workflow). -->

## Now

## Next (max 5, ordered)

## Backlog
T-002 · Add Terraform/ECS V2 plan · (Phase 1)
  VERIFY: docs describe Terraform, VPC, ECR, ECS Fargate, ALB, RDS, CloudWatch, Route53, and ACM migration tasks.

## Done
<!-- Move here with completion date, newest on top: -->
<!-- 2026-07-14 · T-011 · Title -->
2026-08-21 · T-003 · Fix Ansible collection pin for CI
  VERIFY: `ANSIBLE_LOCAL_TEMP=/tmp/ansible-local ANSIBLE_REMOTE_TEMP=/tmp/ansible-remote ansible-galaxy collection install -r ansible/requirements.yml -p /tmp/opsbeacon-ansible-collections-ci2 --force` resolves; `ANSIBLE_COLLECTIONS_PATH=/tmp/opsbeacon-ansible-collections-ci2 ANSIBLE_LOCAL_TEMP=/tmp/ansible-local ANSIBLE_REMOTE_TEMP=/tmp/ansible-remote ansible-playbook -i ansible/inventory.example.ini ansible/playbook.yml --syntax-check` passes; GitHub Actions `CI` on `main` passes.
2026-08-21 · T-001 · Implement OpsBeacon V1
  VERIFY: `.venv/bin/pytest` passed 10 tests; `.venv/bin/ruff check .` passed; `docker compose config` passed; `ANSIBLE_LOCAL_TEMP=/tmp/ansible-local ANSIBLE_REMOTE_TEMP=/tmp/ansible-remote ansible-playbook -i ansible/inventory.example.ini ansible/playbook.yml --syntax-check` passed; `docker compose up --build -d` started db/web/worker; `curl --fail http://localhost:8000/`, `/health`, and `/version` passed.

## Parked / blocked
<!-- Waiting on decision/external thing. Note WHAT unblocks it. -->
