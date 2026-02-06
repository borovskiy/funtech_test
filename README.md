docker compose build --no-cache ap

docker compose --env-file .env up -d
docker compose down
export DATABASE_URL=postgresql+asyncpg://test_user:test_user@localhost:5432/postgres

export BROKER_URL=redis://localhost:6379/0

uv run celery -A app.workers.celery worker --loglevel=info --pool=threads --concurrency=2
uv run python -m app.workers.consumer_faststream


alembic revision --autogenerate
alembic upgrade head