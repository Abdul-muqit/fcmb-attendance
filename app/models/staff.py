from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


if TYPE_CHECKING:
    from app.models.department import Department
    from app.models.role import Role
    from app.models.staff_attendance import StaffAttendance


class Staff(Base):

    __tablename__ = "staff"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    staff_id: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False
    )

    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    department_id: Mapped[int] = mapped_column(
        ForeignKey("departments.id"),
        nullable=False
    )

    role_id: Mapped[int] = mapped_column(
        ForeignKey("roles.id"),
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    department: Mapped["Department"] = relationship(
        back_populates="staff"
    )

    role: Mapped["Role"] = relationship(
        back_populates="staff"
    )

    attendance_records: Mapped[
        list["StaffAttendance"]
    ] = relationship(
        back_populates="staff"
    )