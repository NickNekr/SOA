from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional, Union

class UserDataSchema(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    birth_date: Optional[date]
    email: Optional[EmailStr]
    phone_number: Optional[str]

class LikesStatsSchema(BaseModel):
    task_id: int
    count: int

class ViewsStatsSchema(BaseModel):
    task_id: int
    count: int

class LikesSchema(BaseModel):
    task_id: int
    username: str

class ViewsSchema(LikesSchema):
    pass

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

class TaskIdSchema(BaseModel):
    task_id: Optional[str]

class TaskSchema(BaseModel):
    title: str
    text: str

class FullTaskSchema(TaskIdSchema):
    title: str
    text: str

class DeleteTaskResponse(BaseModel):
    success: bool