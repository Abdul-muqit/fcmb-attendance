from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.department import Department
from app.schemas.department import (
    DepartmentCreate,
    DepartmentResponse,
)


router = APIRouter(
    prefix="/departments",
    tags=["Departments"]
)


@router.post(
    "/",
    response_model=DepartmentResponse
)
def create_department(
    data: DepartmentCreate,
    db: Session = Depends(get_db)
):

    department = Department(
        name=data.name
    )

    db.add(department)
    db.commit()
    db.refresh(department)

    return department


@router.get(
    "/",
    response_model=list[DepartmentResponse]
)
def get_departments(
    db: Session = Depends(get_db)
):

    return db.query(Department).all()