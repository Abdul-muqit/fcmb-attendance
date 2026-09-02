from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


if TYPE_CHECKING:
    from app.models.staff import Staff
    from app.models.role import Role


class Department(Base):

    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    staff: Mapped[list["Staff"]] = relationship(
        back_populates="department"
    )

    roles: Mapped[list["Role"]] = relationship(
        back_populates="department"
    )