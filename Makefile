.PHONY: run up down build stop setup

# Run the application
run:
	. venv/bin/activate && python src/apps/main.py run

# Docker Compose commands
up:
	docker compose up -d

down:
	docker compose down

stop:
    docker compose stop

build:
	docker compose build
