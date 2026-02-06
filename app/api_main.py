import uvicorn
from fastapi import FastAPI

from app.api import order_api, user_api


def create_app() -> FastAPI:
    app = FastAPI(title="ORDERS", version="0.1.0")
    app.include_router(order_api.router, prefix="/api/v1")
    app.include_router(user_api.router, prefix="/api/v1")
    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run("app.api_main:app", host="0.0.0.0", port=9000, reload=True)