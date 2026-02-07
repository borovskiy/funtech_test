from fastapi import HTTPException
from starlette import status


def _not_found_user(email: str):
    return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"User with email: {email} is register")

def _not_found_order(order_id: int):
    return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Order {order_id} not found")


def _wrong_password(email: str):
    return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Wrong password")

def _unauthorized(detail: str = "Not authenticated"):
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )