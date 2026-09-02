from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.db.session import get_db

from app.models.staff import Staff
from app.models.department import Department
from app.models.role import Role

from app.schemas.staff import (
    StaffCreate,
    StaffResponse
)


router = APIRouter(
    prefix="/staff",
    tags=["Staff"]
)


@router.post(
    "/",
    response_model=StaffResponse,
    status_code=status.HTTP_201_CREATED
)
def create_staff(
    data: StaffCreate,
    db: Session = Depends(get_db)
):

    # =========================================================
    # CLEAN INPUT
    # =========================================================

    department_name = data.department.strip()
    role_name = data.role.strip()

    if not department_name:
        raise HTTPException(
            status_code=400,
            detail="Department cannot be empty"
        )

    if not role_name:
        raise HTTPException(
            status_code=400,
            detail="Role cannot be empty"
        )

    # =========================================================
    # CHECK IF STAFF ID ALREADY EXISTS
    # =========================================================

    existing_staff_id = db.query(Staff).filter(
        Staff.staff_id == data.staff_id
    ).first()

    if existing_staff_id:

        raise HTTPException(
            status_code=400,
            detail="Staff ID already exists"
        )

    # =========================================================
    # CHECK IF EMAIL ALREADY EXISTS
    # =========================================================

    existing_email = db.query(Staff).filter(
        Staff.email == data.email
    ).first()

    if existing_email:

        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    # =========================================================
    # FIND DEPARTMENT
    # =========================================================

    department = db.query(Department).filter(
        Department.name.ilike(department_name)
    ).first()

    # =========================================================
    # CREATE DEPARTMENT IF IT DOES NOT EXIST
    # =========================================================

    if not department:

        department = Department(
            name=department_name
        )

        db.add(department)

        # Gives department its ID before creating role
        db.flush()

    # =========================================================
    # FIND ROLE INSIDE THIS DEPARTMENT
    # =========================================================

    role = db.query(Role).filter(
        Role.name.ilike(role_name),
        Role.department_id == department.id
    ).first()

    # =========================================================
    # CREATE ROLE IF IT DOES NOT EXIST
    # =========================================================

    if not role:

        role = Role(
            name=role_name,
            department_id=department.id
        )

        db.add(role)

        db.flush()

    # =========================================================
    # CREATE STAFF
    # =========================================================

    staff = Staff(
        staff_id=data.staff_id,
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        password_hash=hash_password(data.password),
        department_id=department.id,
        role_id=role.id,
        is_active=True
    )

    db.add(staff)

    db.commit()

    db.refresh(staff)

    # =========================================================
    # RETURN STAFF
    # =========================================================

    return staff