from fastapi import FastAPI, Depends

from app.api.qr import router as qr_router
from app.api.auth import router as auth_router
from app.api.attendance import router as attendance_router
from app.api.roles import router as role_router
from app.api.staff import router as staff_router
from app.api.department import router as department_router

from app.core.dependencies import get_current_staff

from app.db.database import Base, engine

from app.models import (
    Department,
    Role,
    Staff,
    StaffAttendance,
)


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="FCMB Attendance Management System",
    version="1.0.0"
)


# =========================
# ROUTERS
# =========================

app.include_router(department_router)

app.include_router(staff_router)

app.include_router(role_router)

app.include_router(attendance_router)

app.include_router(auth_router)

app.include_router(qr_router)


# =========================
# HOME
# =========================

@app.get("/")
def home():

    return {
        "message": "Attendance API is running"
    }


# =========================
# TEST AUTHENTICATION
# =========================

@app.get("/test-auth")
def test_auth(
    current_staff: Staff = Depends(get_current_staff)
):

    return {
        "message": "Authentication successful",
        "staff_id": current_staff.staff_id,
        "name": (
            f"{current_staff.first_name} "
            f"{current_staff.last_name}"
        ),
        "email": current_staff.email
    }