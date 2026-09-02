from datetime import date, datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_staff
from app.db.session import get_db
from app.models.staff import Staff
from app.models.staff_attendance import StaffAttendance


router = APIRouter(
    prefix="/attendance",
    tags=["Attendance"]
)


@router.post("/sign-in")
def sign_in(
    current_staff: Staff = Depends(get_current_staff),
    db: Session = Depends(get_db)
):

    today = date.today()

    attendance = db.query(StaffAttendance).filter(
        StaffAttendance.staff_id == current_staff.id,
        StaffAttendance.attendance_date == today
    ).first()

    if attendance:
        raise HTTPException(
            status_code=400,
            detail="You have already signed in today"
        )

    attendance = StaffAttendance(
        staff_id=current_staff.id,
        attendance_date=today,
        sign_in_time=datetime.now()
    )

    db.add(attendance)
    db.commit()
    db.refresh(attendance)

    return {
        "message": "Sign-in successful",
        "staff_id": current_staff.staff_id,
        "name": f"{current_staff.first_name} {current_staff.last_name}",
        "sign_in_time": attendance.sign_in_time
    }


@router.post("/sign-out")
def sign_out(
    current_staff: Staff = Depends(get_current_staff),
    db: Session = Depends(get_db)
):

    today = date.today()

    attendance = db.query(StaffAttendance).filter(
        StaffAttendance.staff_id == current_staff.id,
        StaffAttendance.attendance_date == today
    ).first()

    if not attendance:
        raise HTTPException(
            status_code=400,
            detail="You have not signed in today"
        )

    if attendance.sign_out_time:
        raise HTTPException(
            status_code=400,
            detail="You have already signed out today"
        )

    attendance.sign_out_time = datetime.now()

    db.commit()
    db.refresh(attendance)

    return {
        "message": "Sign-out successful",
        "staff_id": current_staff.staff_id,
        "name": f"{current_staff.first_name} {current_staff.last_name}",
        "sign_out_time": attendance.sign_out_time
    }


@router.get("/")
def get_attendance(
    db: Session = Depends(get_db)
):

    return db.query(StaffAttendance).all()

@router.get("/my-history")
def my_history(
    current_staff: Staff = Depends(get_current_staff),
    db: Session = Depends(get_db)
):

    records = db.query(
        StaffAttendance
    ).filter(
        StaffAttendance.staff_id == current_staff.id
    ).order_by(
        StaffAttendance.attendance_date.desc()
    ).all()

    return [
        {
            "date": record.attendance_date,
            "sign_in_time": record.sign_in_time,
            "sign_out_time": record.sign_out_time
        }
        for record in records
    ]

@router.get("/admin/all")
def get_all_attendance(
    current_staff: Staff = Depends(get_current_staff),
    db: Session = Depends(get_db)
):

    if current_staff.role_id != 1:
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return db.query(StaffAttendance).all()


@router.get("/today")
def get_today_attendance(
    current_staff: Staff = Depends(get_current_staff),
    db: Session = Depends(get_db)
):

    today = date.today()

    records = db.query(StaffAttendance).filter(
        StaffAttendance.attendance_date == today
    ).all()

    return {
        "date": today,
        "total_records": len(records),
        "signed_in": sum(
            1 for record in records
            if record.sign_in_time is not None
        ),
        "signed_out": sum(
            1 for record in records
            if record.sign_out_time is not None
        ),
        "records": records
    }