.PHONY: all run

all: run

run:
	export ENVIROMENT=local
	gunicorn main:app --worker-class uvicorn.workers.UvicornWorker --config infra/gunicorn.conf.py --reload

migrate-create:
	alembic revision --autogenerate -m $(MIGRATION)

migrate-apply:
	alembic upgrade head

docker-up:
	docker compose up -d

docker-down:
	docker compose down

docker-test-up:
	docker compose -f docker-compose.test.yml up -d

docker-test-down:
	docker compose -f docker-compose.test.yml down
