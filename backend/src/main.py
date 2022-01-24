import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from typing import Callable
from src.api.routes.handlers import router as api_router
from src.settings import get_app_settings, AppSettings
from src.db.events import connect_to_db, close_db_connection


def _create_start_app_handler(
    app: FastAPI,
    settings: AppSettings,
) -> Callable:  # type: ignore
    async def start_app() -> None:
        await connect_to_db(app, settings)

    return start_app


def _create_stop_app_handler(app: FastAPI) -> Callable:  # type: ignore
    async def stop_app() -> None:
        await close_db_connection(app)

    return stop_app


def get_app() -> FastAPI:
    settings = get_app_settings()

    app = FastAPI(**settings.fastapi_init_args)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_hosts,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix=settings.api_prefix)

    app.add_event_handler(
        "startup",
        _create_start_app_handler(app, settings),
    )
    app.add_event_handler(
        "shutdown",
        _create_stop_app_handler(app),
    )

    return app


app = get_app()
