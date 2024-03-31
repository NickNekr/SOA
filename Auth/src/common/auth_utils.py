from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from typing import Annotated, Union, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from database.model import User
from database.session import get_session
from config import get_config
from common.repository import get_user_repo
from common.exception import UNAUTHORIZED
from common.schema import TokenData



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

user_repo = get_user_repo()
app_config = get_config()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

async def authenticate_user(username: str, password: str, session: AsyncSession):
    user: Optional[User]  = await user_repo.get_user(username, session)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, app_config.FastApi.SECRET_KEY, algorithm=app_config.FastApi.ALGORITHM)
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: Annotated[AsyncSession, Depends(get_session)]):
    try:
        payload = jwt.decode(token, app_config.FastApi.SECRET_KEY, algorithms=[app_config.FastApi.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise UNAUTHORIZED
        token_data = TokenData(username=username)
    except JWTError:
        raise UNAUTHORIZED

    user: User = await user_repo.get_user(token_data.username, session)

    if user is None:
        raise UNAUTHORIZED

    return user
