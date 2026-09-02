from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import (
    verify_password,
    create_access_token
)
from app.db.session import get_db
from app.models.staff import Staff
from app.schemas.auth import LoginRequest


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/login")
def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
):

    # Find staff by email
    staff = db.query(Staff).filter(
        Staff.email == data.email
    ).first()

    # Staff does not exist
    if not staff:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Check password
    if not verify_password(
        data.password,
        staff.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Check if account is active
    if not staff.is_active:
        raise HTTPException(
            status_code=403,
            detail="Staff account is inactive"
        )

    # Create JWT token
    access_token = create_access_token(
        staff.id
    )

    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer",
        "staff_id": staff.staff_id,
        "name": f"{staff.first_name} {staff.last_name}"
    }