.PHONY: run up down build stop, migrate, test

# Run the application

run:
	cd src/apps && python3 main.py run

# Docker Compose commands
up:
	docker compose up -d

down:
	docker compose down --volumes


build:
	docker compose up --build -d

stop:
	docker compose stop


migrate:
	cd src/apps && alembic revision --autogenerate -m "Database creation"

test:
	PYTHONPATH=src/apps pytest -v -s