Описание задачи по ссылке
https://docs.google.com/document/d/1BpDSybzNuRQViZ99MVHcnoGSgu8GOy07GkMQOpNTxMM/edit?tab=t.0



для начала стартуем все проекты командой
docker compose --env-file full_compose.env up -d

Далее переходим на http://localhost:9000/docs
там все роуты по задаче





docker compose build --no-cache ap
docker compose --env-file .env up -d
docker compose down
export DATABASE_URL=postgresql+asyncpg://test_user:test_user@localhost:5432/postgres


local_start
export REDIS_HOST=localhost
export REDIS_PORT=6379
export REDIS_DB_CACHE=1
export REDIS_DB_CELERY=0
uv run --env-file .env celery -A app.workers.celery worker --loglevel=info --pool=threads --concurrency=2

export REDIS_HOST=localhost
export REDIS_PORT=6379
export REDIS_DB_CACHE=1
export REDIS_DB_CELERY=0
export KAFKA_HOST=localhost
export KAFKA_PORT=9094
uv run --env-file .env python -m app.workers.consumer_faststream



alembic revision --autogenerate
uv run --env-file .env alembic upgrade head

