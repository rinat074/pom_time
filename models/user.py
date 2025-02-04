from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from .base import Base

class UserProfile(Base):
    __tablename__ = "UserProfile"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
