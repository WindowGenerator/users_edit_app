import asyncpg
from fastapi import FastAPI
import logging
from src.settings import AppSettings
from src.db.database import async_session
from src.db.models import User
from sqlalchemy import select

logger = logging.getLogger(__name__)


async def connect_to_db(app: FastAPI, settings: AppSettings) -> None:
    logger.info(f"Connecting to {settings.asyncpg_url}")

    app.state.db = await async_session(settings.asyncpg_url)
    
    logger.info("Connection established")


# TODO: по человечески закрывать 
async def close_db_connection(app: FastAPI) -> None:
    logger.info("Closing connection to database")

    await app.state.db.close()

    logger.info("Connection closed")