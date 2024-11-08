from fastapi import APIRouter

from app.users.manager import auth_backend, fastapi_users
from app.users.schemas import UserCreate, UserRead, UserUpdate

user_router = APIRouter()

user_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
user_router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"]
)
user_router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    tags=["users"],
)
