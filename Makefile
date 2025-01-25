.PHONY: all run

all: run

run:
	uvicorn main:app --reload --env-file=.local.env

migrate-create:
	alembic revision --autogenerate -m $(MIGRATION)

migrate-apply:
	alembic upgrade head

docker-up:
	docker compose up -d

docker-down:
	docker compose down
