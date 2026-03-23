from typing import Annotated
from fastapi import APIRouter
from ..schemas import UserCreate, UserResponse


auth_router = APIRouter()


@auth_router.post("/signup")
async def create_account(data: UserCreate) -> UserResponse:
    pass


@auth_router.post("/login/")
async def login(username, password):
    pass
