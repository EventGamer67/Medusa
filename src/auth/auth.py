from fastapi import APIRouter, HTTPException, Depends, Request
from my_secrets import SECRET, API_KEY  # добавьте сюда ваш API ключ
from src.auth.schemas import UserRead, UserCreate
import uuid
from typing import Optional
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from src.alchemy.db_helper import local_db_helper
from src.auth.schemas import User

router = APIRouter()


# Зависимость для проверки API ключа
async def api_key_auth(request: Request):
    api_key = request.headers.get("X-API-KEY")
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")


# Получение базы данных пользователей
async def get_user_db(
    session: AsyncSession = Depends(local_db_helper.session_dependency),
):
    yield SQLAlchemyUserDatabase(session, User)


# Менеджер пользователей
class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])
current_active_user = fastapi_users.current_user(active=True)

# Включаем маршруты для FastAPI Users
router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/jwt",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="",
    tags=["auth"],
)


# Авторизация по ролям и API Key
def authorize(roles):
    def decorator(func):
        async def wrapper(
            request: Request,
            current_user: Optional[User] = Depends(current_active_user),
        ):
            print(request.headers)

            # Проверка на API Key
            api_key = request.headers.get("X-API-KEY")
            if api_key != API_KEY:
                raise HTTPException(status_code=403, detail="Invalid API Key")

            # Проверка роли пользователя
            if current_user.role not in roles:
                raise HTTPException(status_code=403, detail="Unauthorized")

            return await func()

        return wrapper

    return decorator


# Пример защищённого маршрута с проверкой роли и API Key
@router.get("/protected-route", tags=["Users"])
@authorize(roles=["Owner"])
async def protected_route():
    return {"message": "Hello, this is a protected route!"}
