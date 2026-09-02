from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import Date, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

if TYPE_CHECKING:
    from app.models.staff import Staff


class StaffAttendance(Base):
    __tablename__ = "staff_attendance"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    staff_id: Mapped[int] = mapped_column(
        ForeignKey("staff.id"),
        nullable=False
    )

    attendance_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    sign_in_time: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    sign_out_time: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    staff: Mapped["Staff"] = relationship(
        back_populates="attendance_records"
    )




