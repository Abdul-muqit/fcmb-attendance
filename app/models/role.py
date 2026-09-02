from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    DateTime,
    ForeignKey,
    String,
    UniqueConstraint
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from app.db.database import Base


if TYPE_CHECKING:
    from app.models.staff import Staff
    from app.models.department import Department


class Role(Base):

    __tablename__ = "roles"

    __table_args__ = (
        UniqueConstraint(
            "department_id",
            "name",
            name="uq_role_department_name"
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    department_id: Mapped[int] = mapped_column(
        ForeignKey("departments.id"),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    department: Mapped["Department"] = relationship(
        back_populates="roles"
    )

    staff: Mapped[list["Staff"]] = relationship(
        back_populates="role"
    )