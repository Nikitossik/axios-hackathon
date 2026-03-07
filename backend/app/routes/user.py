from fastapi import Depends, status, APIRouter, Query
from sqlalchemy.orm import Session
from typing import Annotated

from ..dependencies import get_db, get_current_user
from ..models.user import User
from ..schemas.shared import PaginatedResponse, BaseQueryParams
from ..schemas.user import (
    UserIn,
    UserOut,
    UserUpdate
)
from ..schemas.user_profile import UserProfileIn
from ..services import UserService

# Router: Users CRUD, authentication helpers, and profile access
user_router = APIRouter(prefix="/api/user", tags=["Users"])

@user_router.get(
    "/",
    response_model=PaginatedResponse[UserOut],
    summary="List users",
    description="Return a paginated list of users. Supports pagination, sorting, and filters (user_roles, user_types, q).",
)
async def get_users(
    *, db: Session = Depends(get_db), query_params: Annotated[BaseQueryParams, Query()]
):
    return UserService(db).get_paginated(query_params)


@user_router.get(
    "/me",
    response_model=UserOut,
    summary="Get current user",
    description="Return the currently authenticated user resolved from the Bearer token.",
)
async def get_user_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user


@user_router.get(
    "/{user_id}",
    response_model=UserOut,
    summary="Get user by ID",
    description="Retrieve a single user by its unique identifier.",
)
async def get_user_by_id(*, user_id: int, db: Session = Depends(get_db)):
    return UserService(db).get_by_id(user_id)


@user_router.post(
    "/",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a user",
    description="Create a new user. For base users, a role-specific profile (student/professor) is provisioned. Admin-only.",
)
async def create_user(user: UserIn, db: Session = Depends(get_db)):
    return UserService(db).create(user)


@user_router.post(
    "/{user_id}/profile",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a user profile",
    description="Create a new user profile for a given user ID. Admin-only.",
)
async def create_user_profile(user_id: int, profile: UserProfileIn, db: Session = Depends(get_db)):
    return UserService(db).create_profile(user_id, profile)


@user_router.put(
    "/{user_id}",
    response_model=UserOut,
    summary="Replace a user",
    description="Replace all fields of an existing user by ID. Admin-only.",
)
async def update_user(user_id: int, user: UserIn, db: Session = Depends(get_db)):
    return UserService(db).update(user_id, user)


@user_router.patch(
    "/{user_id}",
    response_model=UserOut,
    summary="Partially update a user",
    description="Apply a partial update to a user by ID. Admin-only.",
)
async def modify_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    return UserService(db).update(user_id, user)


@user_router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a user",
    description="Delete a user by ID. Prevents deletion of the last admin. Returns 204 No Content on success. Admin-only.",
)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    return UserService(db).delete(user_id)