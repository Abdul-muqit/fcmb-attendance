from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.role import Role


router = APIRouter(
    prefix="/roles",
    tags=["Roles"]
)


@router.post("/")
def create_role(
    name: str,
    db: Session = Depends(get_db)
):

    role = Role(name=name)

    db.add(role)
    db.commit()
    db.refresh(role)

    return role


@router.get("/")
def get_roles(
    db: Session = Depends(get_db)
):

    return db.query(Role).all()