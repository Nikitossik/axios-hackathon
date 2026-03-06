from fastapi import Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated

from ..services import UserService
from ..dependencies import get_db
from ..schemas.user import Token, RefreshTokenIn
import app.utils.security as security


auth_router = APIRouter(prefix="/api/auth", tags=["Auth"])


@auth_router.post(
    "/token",
    summary="Obtain access/refresh token pair",
    description=(
    	"Authenticate with OAuth2 Password flow and receive a JWT access token and refresh token.\n\n"
        "Form fields:\n"
        "- username: user email\n"
        "- password: user password"
    ),
)	
async def login_for_token_pair(
    *,
    db: Session = Depends(get_db),
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    """Authenticate user and return access and refresh tokens."""
    user = UserService(db).authenticate(
        user_email=form_data.username, user_password=form_data.password
    )

    data_to_encode = {"sub": str(user.id)}

    access_token = security.create_token(data=data_to_encode)

    refresh_token = security.create_token(
        data=data_to_encode,
        token_type="refresh",
    )
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )


@auth_router.post(
    "/refresh",
    summary="Refresh access token",
    description=(
        "Validate a refresh token and issue a new JWT access token. "
        "The original refresh token remains valid and is returned unchanged."
    ),
)
async def refresh_token(*, refresh: RefreshTokenIn):
    """Refresh access token using a valid refresh token."""
    refresh_token = refresh.model_dump().get("refresh_token")

    payload = security.decode_token(refresh_token, token_type="refresh")

    user_id = payload.get("sub")

    new_token = security.create_token(data={"sub": str(user_id)})
    return Token(
        access_token=new_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )