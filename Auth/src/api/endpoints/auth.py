from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from common.schema import Token, UserDataSchema, UserLoginSchema

from Auth.src.utils.model_repository import get_user_repo, get_user_data_repo, BaseRepository
from Auth.src.utils.exception import USERNAME_ALREADY_TAKEN, WRONG_USERNAME_OR_PASS
from Auth.src.utils.auth_utils import authenticate_user, create_access_token, get_password_hash, get_current_user

from Auth.src.database.session import get_session
from Auth.src.database.model import User, UserData
from Auth.src.config import get_config

app_config = get_config()

auth_router = APIRouter(prefix="/auth")


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
    user: UserLoginSchema, session: AsyncSession = Depends(get_session), user_repo: BaseRepository = Depends(get_user_repo), user_data_repo: BaseRepository = Depends(get_user_data_repo)
):
    existing_user = await user_repo.get_by_condition(User.username == user.username, session)
    if existing_user:
        raise USERNAME_ALREADY_TAKEN

    hashed_password = get_password_hash(user.password)
    user.password = hashed_password

    empty_user_data = UserData()
    await user_data_repo.add_model_instance(empty_user_data, session)

    new_user = User(
            username=user.username,
            hashed_password=user.password,
            user_data_id=empty_user_data.id
        )
    await user_repo.add_model_instance(new_user, session)

    return {"message": f"User registered successfully with id: {new_user.id}"}

@auth_router.put("/change_user_data/")
async def change_user_data(
    current_user: Annotated[User, Depends(get_current_user)],
    user_data: UserDataSchema,
    session: AsyncSession = Depends(get_session),
    user_data_repo: BaseRepository = Depends(get_user_data_repo)
):
    await user_data_repo.update_model_by_schema(current_user.user_data, user_data, session)

    return {"message": f"User: {current_user.username} was updated!"}