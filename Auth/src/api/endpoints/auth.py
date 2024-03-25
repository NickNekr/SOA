from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from typing import Annotated, Union, Optional
from sqlalchemy.ext.asyncio import AsyncSession

from common.schema import TokenData, Token, UserDataSchema, UserLoginSchema
from common.exception import UNAUTHORIZED, USERNAME_ALREADY_TAKEN, WRONG_USERNAME_OR_PASS
from common.repository import get_user_repo

from database.session import get_session
from database.model import User


from config import get_config

app_config = get_config()
user_repo = get_user_repo()

auth_router = APIRouter(prefix="/auth")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



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




@auth_router.post("/")
async def authenticate(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: AsyncSession = Depends(get_session)
) -> Token:
    user = await authenticate_user(form_data.username, form_data.password, session)

    if not user:
        raise WRONG_USERNAME_OR_PASS 
    access_token_expires = timedelta(minutes=app_config.FastApi.ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")

@auth_router.post("/register/")
async def register_user(
    user: UserLoginSchema, session: AsyncSession = Depends(get_session)
):
    existing_user = await user_repo.get_user(user.username, session)
    if existing_user:
        raise USERNAME_ALREADY_TAKEN

    hashed_password = get_password_hash(user.password)
    user.password = hashed_password

    user_id = await user_repo.create_user(user, session)
  
    return {"message": f"User registered successfully with id: {user_id}"}

@auth_router.put("/change_user_data/")
async def change_user_data(
    current_user: Annotated[User, Depends(get_current_user)],
    user_data: UserDataSchema,
    session: AsyncSession = Depends(get_session)
):
    
    current_user.user_data.change_user_data(user_data)
    await session.commit()

    return {"message": f"User: {current_user.username} was updated!"}