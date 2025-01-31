from typing import Annotated
from fastapi import APIRouter, Depends
from schema.user import UserCreateSchema, UserLoginSchema
from service import UserService
from dependency import get_user_service

router = APIRouter(prefix="/user", tags=["user"])

@router.post("/")
async def create_user(body: UserCreateSchema, user_service: Annotated[UserService, Depends(get_user_service)]):
    return await user_service.create_user(body.username, body.password)

@router.post("/login")
async def login_user(user: UserLoginSchema, user_service: Annotated[UserService, Depends(get_user_service)]):
    return await user_service.login_user(user)

