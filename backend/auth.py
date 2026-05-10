from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException, Header
from jose import JWTError

SECRET_KEY = "SECRET123"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password):
    return pwd_context.hash(password)


def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)


def create_token(data: dict):
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(days=1)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(authorization: str = Header(None)):

    if not authorization:
        raise HTTPException(status_code=401, detail="Missing token")

    try:
        token = authorization.split(" ")[1]
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def admin_required(user):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admins only")
    return user