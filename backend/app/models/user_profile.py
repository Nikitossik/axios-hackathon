from __future__ import annotations
from ..database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Enum, ForeignKey, Integer
from ..utils.enums import UserGenderEnum, UserAgeGroupEnum, UserDrivingStyleEnum

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User 


class UserProfile(Base):
    __tablename__ = "user_profile"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), primary_key=True
    )
    driving_style: Mapped[UserDrivingStyleEnum | None] = mapped_column(Enum(UserDrivingStyleEnum, create_constraint=True, name="user_driving_style_enum"), nullable=True)
    age_group: Mapped[UserAgeGroupEnum] = mapped_column(Enum(UserAgeGroupEnum, create_constraint=True, name="user_age_group_enum"))
    driving_experience_years: Mapped[int] = mapped_column(Integer)
    gender_identity: Mapped[UserGenderEnum] = mapped_column(Enum(UserGenderEnum, create_constraint=True, name="user_gender_enum"))
    gender_self_description: Mapped[str] = mapped_column(String(100), nullable=True)
    
    user: Mapped["User"] = relationship("User", back_populates="profile", uselist=False)