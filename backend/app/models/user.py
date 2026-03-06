from __future__ import annotations
from ..database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Enum

from typing import TYPE_CHECKING


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )  # Unique numeric identifier (primary key)
    name: Mapped[str] = mapped_column(String(100))  # First name (given name)
    surname: Mapped[str] = mapped_column(String(100))  # Last name (family name)
    email: Mapped[str] = mapped_column(
        String(100), unique=True, index=True
    )  # Login email; unique and indexed
    password_hash: Mapped[str] = mapped_column(
        String(256)
    )  # Secure password hash (never store plaintext)