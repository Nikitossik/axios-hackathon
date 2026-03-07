from pydantic import BaseModel, Field

class Token(BaseModel):
    """
    Authentication token pair returned after successful login or refresh.
    """

    access_token: str = Field(
        ...,
        description="JWT access token for authenticated requests.",
        examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."],
    )
    refresh_token: str = Field(
        ...,
        description="JWT refresh token used to obtain a new access token.",
        examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.refresh..."],
    )
    token_type: str = Field(
        ...,
        description='Token type hint for clients (typically "bearer").',
        examples=["bearer"],
    )


class TokenData(BaseModel):
    """
    Decoded token payload used internally for authorization.
    """

    sub: str = Field(
        ...,
        description="Subject (user identifier) embedded in the token.",
        examples=["5"],
    )
    role: str = Field(
        ...,
        description="User role embedded in the token.",
        examples=["user"],
    )
    exp: int = Field(
        ...,
        description="Expiration time as a UNIX timestamp (seconds).",
        examples=[1732051200],
    )


class RefreshTokenIn(BaseModel):
    """
    Input schema for refreshing an access token using a refresh token.
    """

    refresh_token: str = Field(
        ...,
        description="JWT refresh token issued during authentication.",
        examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.refresh..."],
    )