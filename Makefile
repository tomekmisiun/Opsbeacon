.PHONY: up down logs test lint migrate revision seed compose-check ansible-check ansible-setup ansible-ping ansible-deploy ansible-dry-run

up:
	docker compose up --build

down:
	docker compose down

logs:
	docker compose logs -f

test:
	pytest

lint:
	ruff check .

migrate:
	alembic upgrade head

revision:
	alembic revision --autogenerate -m "$(m)"

seed:
	python -m app.seed

compose-check:
	docker compose config

ansible-check:
	ansible-playbook -i ansible/inventory.example.ini ansible/playbook.yml --syntax-check

ansible-setup:
	ansible-galaxy collection install -r ansible/requirements.yml

ansible-ping:
	ansible -i ansible/inventory.ini production -m ansible.builtin.ping

ansible-deploy:
	ansible-playbook -i ansible/inventory.ini ansible/playbook.yml

ansible-dry-run:
	ansible-playbook -i ansible/inventory.ini ansible/playbook.yml --check --diff
