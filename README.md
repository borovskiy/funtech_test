docker compose build --no-cache ap

docker compose --env-file .env up -d
docker compose down
export DATABASE_URL=postgresql+asyncpg://test_user:test_user@localhost:5432/postgres

export BROKER_URL=redis://localhost:6379/0

celery -A app.worker.celery:app worker --loglevel=info
celery -A app.worker.celery:app beat --loglevel=info



alembic revision --autogenerate
alembic upgrade head