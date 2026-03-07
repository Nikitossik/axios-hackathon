from .base import BaseRepository
from ..models import User, UserProfile


class UserRepository(BaseRepository):
    """Repository for User entities, providing common queries on top of BaseRepository."""

    model = User  # Underlying SQLAlchemy model for this repository

    def get_by_email(self, user_email: str) -> User | None:
        """
        Retrieve a single user by email.

        Args:
            user_email (str): Email address to match (unique).

        Returns:
            User | None: The matching user, or None if not found.
        """
        return self.db.query(User).filter(User.email == user_email).first()



class UserProfileRepository(BaseRepository):
    """Repository for UserProfile entities, providing common queries on top of BaseRepository."""

    model = UserProfile