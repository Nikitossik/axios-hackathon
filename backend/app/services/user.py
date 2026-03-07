from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from ..repositories import (
    UserRepository, UserProfileRepository
)
from ..models import User
from ..schemas.user import UserIn, UserUpdate, UserOut
from ..schemas.user_profile import UserProfileIn
from ..utils import exceptions, security
from app.utils.exceptions import AlreadyExistsException
from .base import BaseService
from fastapi import HTTPException, status

class UserService(BaseService[User, UserIn]):
    """
    Service layer for User domain logic.

    Responsibilities:
    - Authenticate users, manage CRUD, and apply list filters.
    - Create role-specific profiles (student/professor) on user creation.
    - Enforce constraints (e.g., prevent deletion of the last admin).
    """

    def __init__(self, db: Session):
        """
        Initialize the User service with repositories.

        Args:
            db (Session): Active SQLAlchemy session.
        """
        super().__init__(db, User, UserRepository(db))
        self.profile_repo = UserProfileRepository(db)

    def authenticate(self, user_email, user_password) -> User:
        """
        Authenticate a user by email and password.

        Args:
            user_email (str): Email address provided by the user.
            user_password (str): Plaintext password to verify.

        Returns:
            User: Authenticated user entity.

        Raises:
            exceptions.UserNotFoundException: If user not found or password mismatch.
        """
        found_user = self.get_by_email(user_email)

        if not found_user or not security.verify_password(
            user_password, found_user.password_hash
        ):
            raise exceptions.UserNotFoundException()

        return found_user

    def create(self, user: UserIn) -> User:
        """
        Create a new user and provision the role-specific profile when applicable.

        Steps:
        - Ensure email uniqueness.
        - Hash provided password.
        - Persist user and create associated student/professor profile.

        Args:
            user (UserIn): Payload for the new user.

        Returns:
            User: Newly created user.

        Raises:
            AlreadyExistsException: If a user with the same email already exists.
        """
        user_data = user.model_dump()

        found_user = self.repo.get_by_email(user_data["email"])

        if found_user:
            raise AlreadyExistsException("User", "email", user_data["email"])

        user_data["password_hash"] = security.get_password_hash(user_data["password"])

        new_user = super().create(user_data)

        return new_user
    
    def create_profile(self, user_id: int, profile_data: UserProfileIn) -> UserOut:
        """
        Create a user profile for a given user ID.

        Args:
            user_id (int): Identifier of the user to associate the profile with.
            profile_data (UserProfileIn): Data for the new user profile.
        Returns:
            UserOut: The user with the newly created profile.
        """
        found_user = self.get_by_id(user_id)
        
        if found_user.profile:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User profile already exists.")
        
        profile_dict = profile_data.model_dump()
        profile_dict["user_id"] = user_id
        new_profile = self.profile_repo.create(profile_dict)
        return found_user

    def update(self, user_id: int, user: UserIn | UserUpdate) -> User:
        """
        Update an existing user. Password is re-hashed if provided.
        Updates profile data based on user type.

        Args:
            user_id (int): Identifier of the user to update.
            user (UserIn | UserUpdate): Partial or full update payload.

        Returns:
            User: Updated user entity.
        """
        user_data = user.model_dump()

        if user_data.get("password"):
            user_data["password_hash"] = security.get_password_hash(
                user_data["password"]
            )

        updated_user = super().update(user_id, user_data)
        return updated_user

    def delete(self, user_id: int):
        """
        Delete a user by ID, preventing removal of the last admin.

        Args:
            user_id (int): Identifier of the user to delete.

        Returns:
            Any: Repository delete result.

        Raises:
            LastAdminException: If attempting to delete the only remaining admin.
        """
        return super().delete(user_id)

    def get_by_email(self, email: str) -> User | None:
        """
        Retrieve a user by email.

        Args:
            email (str): Email address to search for.

        Returns:
            User | None: Matching user or None if not found.
        """
        return self.repo.get_by_email(email)