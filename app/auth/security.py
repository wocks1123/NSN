from jose import JWTError, jwt
from fastapi import HTTPException, status
from starlette.requests import Request

from app.core.config import settings

from .schemas import JWTUser


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def verify_token(token: str) -> JWTUser:
    try:
        print(">>> payload....", token)
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        print(">>> payload", payload)
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        return JWTUser(user_id=user_id)
    except JWTError:
        raise credentials_exception


def get_current_user(request: Request) -> JWTUser:
    authorization_header = request.headers.get("Authorization")
    if not authorization_header:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    token = authorization_header.replace("Bearer ", "")
    return verify_token(token)
