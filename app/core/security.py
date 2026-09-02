from datetime import datetime, timedelta, timezone

from jose import jwt
from pwdlib import PasswordHash


password_hash = PasswordHash.recommended()


SECRET_KEY = "demo-secret-key-change-in-production"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 300


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(
    password: str,
    hashed_password: str
) -> bool:

    return password_hash.verify(
        password,
        hashed_password
    )


def create_access_token(staff_id: int) -> str:

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(staff_id),
        "exp": expire
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )