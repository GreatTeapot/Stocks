from typing import Union

from fastapi import APIRouter
from starlette.responses import Response

from api.dependencies.dependencies import UserServiceDep, UserUOWDep, UserDep
from core.constants import REFRESH
from core.security import Security
from modules.users.responses import user as responses
from modules.users.schemas.auth import TokenInfoSchema
from modules.users.schemas.user import (
    RegisterSchema,
    UpdateUserSchema,
    CurrentUserSchema, UserResponseSchema
)

user = APIRouter(prefix="/api/v1/user", tags=["User"])


@user.post("/register",
           summary="Register a new user",
           responses=responses.REGISTRATION_RESPONSES)
async def create_user(
    uow: UserUOWDep,
    service: UserServiceDep,
    model: RegisterSchema,
    response: Response,
) -> TokenInfoSchema:
    """Controller for registering a new user"""
    user_data = await service.create(uow, model)
    access_token = Security.create_access_token(user_data)
    refresh_token = Security.create_refresh_token(user_data)
    response.set_cookie(key=REFRESH,
                        value=refresh_token,
                        httponly=True,
                        secure=False)
    return TokenInfoSchema(access_token=access_token, )


@user.get("/profile",
          summary="User profile",
          responses=responses.GET_RESPONSES)
async def get_user_profile(
    uow: UserUOWDep,
    service: UserServiceDep,
    current_user: UserDep,
) -> Union[UpdateUserSchema, UserResponseSchema]:
    """Controller for retrieving the current user's profile"""
    user_data = await service.get_user(uow, current_user.id)
    return user_data


@user.patch("/profile",
            summary="User profile edit",
            responses=responses.EDIT_RESPONSES)
async def edit_user_profile(
        uow: UserUOWDep,
        service: UserServiceDep,
        current_user: UserDep,
        model: UpdateUserSchema
) -> UpdateUserSchema:
    """Controller for editing the current user's profile"""
    result = await service.update(uow, model, current_user.id)
    return result

@user.get("/{user_id}",
          summary="User profile by id",
          responses=responses.GET_RESPONSES)
async def get_user_profile_by_id(
    uow: UserUOWDep,
    service: UserServiceDep,
    user_id: int,
) -> CurrentUserSchema:
    """Controller for retrieving the user's profile by id"""
    user_data = await service.get_user(uow, user_id)
    return user_data

