from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.security import SECRET_KEY, ALGORITHM
from app.db.session import get_db
from app.models.staff import Staff


security = HTTPBearer()


def get_current_staff(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> Staff:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={
            "WWW-Authenticate": "Bearer"
        }
    )

    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        staff_id = payload.get("sub")

        if staff_id is None:
            raise credentials_exception

        staff_id = int(staff_id)

    except (JWTError, ValueError):
        raise credentials_exception

    staff = db.query(Staff).filter(
        Staff.id == staff_id
    ).first()

    if staff is None:
        raise credentials_exception

    if not staff.is_active:
        raise HTTPException(
            status_code=403,
            detail="Staff account is inactive"
        )

    return staff