from datetime import datetime

from pydantic import BaseModel


class AttendanceResponse(BaseModel):
    id: int
    staff_id: int
    attendance_date: str
    sign_in_time: datetime | None
    sign_out_time: datetime | None

    model_config = {
        "from_attributes": True
    }