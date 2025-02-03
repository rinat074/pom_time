from fastapi import APIRouter, Depends
from schema import UserLoginSchema, UserCreateSchema
from service import AuthService
from dependency import get_auth_service
from typing import Annotated
from exception import UserNotFoundError, UserPasswordError
from fastapi import HTTPException

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post(
        "/login",
        response_model=UserLoginSchema
        )
async def login(user: UserCreateSchema, auth_service: Annotated[AuthService, Depends(get_auth_service)]):
    try:
        user_login_data = await auth_service.login(user.username, user.password)
        return user_login_data
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.detail)
    except UserPasswordError as e:
        raise HTTPException(status_code=401, detail=e.detail)
