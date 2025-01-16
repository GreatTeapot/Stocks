.PHONY: run up down build stop

# Run the application

run:
	cd src/apps && python3 main.py run

# Docker Compose commands
up:
	docker compose up -d

down:
	docker compose down --volumes


build:
	docker compose up --build

stop:
	docker compose stop
