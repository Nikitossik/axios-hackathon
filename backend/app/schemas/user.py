from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    model_validator,
    field_serializer,
)
from typing import Annotated
from typing_extensions import Self
from .shared import BaseQueryParams, BaseFilterParams
from .user_profile import UserProfileUpdate, UserProfileOut

class UserBase(BaseModel):
    """
    Base schema for User data shared by input/output models.
    Captures identity, role, and optional user type classification.
    """

    model_config = ConfigDict(from_attributes=True)

    email: Annotated[
        str,
        Field(
            max_length=100,
            description="Unique email address used for login.",
            examples=["user@example.com"],
        ),
    ]
    name: Annotated[
        str,
        Field(
            max_length=100,
            description="First (given) name of the user.",
            examples=["Ada"],
        ),
    ]
    surname: Annotated[
        str,
        Field(
            max_length=100,
            description="Last (family) name of the user.",
            examples=["Lovelace"],
        ),
    ]


class UserIn(UserBase):
    """
    Input schema for creating a User.
    Includes password and optional group association for students.
    """

    password: Annotated[
        str,
        Field(
            min_length=6,
            description="Plaintext password for account creation (will be hashed).",
            examples=["s3cr3tPwd"],
        ),
    ]


class UserUpdate(BaseModel):
    """
    Partial update schema for User; all fields are optional.
    """

    model_config = ConfigDict(from_attributes=True)

    password: Annotated[
        str | None,
        Field(
            None,
            min_length=6,
            description="Optional new plaintext password (will be hashed).",
            examples=["n3wS3cr3t"],
        ),
    ]
    name: Annotated[
        str | None,
        Field(
            None,
            max_length=100,
            description="Optional new first name.",
            examples=["Grace"],
        ),
    ]
    surname: Annotated[
        str | None,
        Field(
            None,
            max_length=100,
            description="Optional new last name.",
            examples=["Hopper"],
        ),
    ]
    
    profile: UserProfileUpdate | None = Field(
        None,
        description="Optional profile information to update alongside user data.",
    )


class UserOut(UserBase):
    """
    Output schema for User including identifiers and optional role-specific profiles.
    """

    id: int = Field(
        ...,
        description="Unique identifier of the user.",
        examples=[5],
    )
    profile: UserProfileOut | None = Field(
        None,
        description="Optional profile information for the user.",
    )
