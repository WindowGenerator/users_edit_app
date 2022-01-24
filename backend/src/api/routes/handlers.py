from fastapi import APIRouter

from src.api.routes import users, authentication

router = APIRouter()
router.include_router(authentication.router, tags=["authentication"])
router.include_router(users.router, tags=["users"])
