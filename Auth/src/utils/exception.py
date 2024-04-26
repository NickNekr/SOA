from fastapi import HTTPException, status

UNAUTHORIZED = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

USERNAME_ALREADY_TAKEN = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username is already taken",
        )


WRONG_USERNAME_OR_PASS = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or password was wrong"
        )