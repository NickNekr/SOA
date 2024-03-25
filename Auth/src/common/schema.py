from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional, Union

class UserDataSchema(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    birth_date: Optional[date]
    email: Optional[EmailStr]
    phone_number: Optional[str]


class UserUpdateSchema(BaseModel):
    user_data: UserDataSchema

class UserLoginSchema(BaseModel):
    username: str
    password: str

class UserSchema(UserLoginSchema, UserDataSchema):
    pass

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None