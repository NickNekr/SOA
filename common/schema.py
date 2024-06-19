from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional, Union, List
from uuid import UUID

class UserDataSchema(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    birth_date: Optional[date]
    email: Optional[EmailStr]
    phone_number: Optional[str]

class LikesStatsSchema(BaseModel):
    task_id: str
    count: int

class ViewsStatsSchema(BaseModel):
    task_id: str
    count: int
    author: Optional[str]

class LikesSchema(BaseModel):
    task_id: str
    username: str
    author: Optional[str]

class TaskToAuthorSchema(BaseModel):
    task_id: UUID 
    author: str

    class Config:
        orm_mode = True

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

class TaskRequest(BaseModel):
    task_id: str

class TaskStatsResponse(BaseModel):
    task_id: str
    views: int
    likes: int

class TopTasksRequest(BaseModel):
    sort_by: str  # 'views' or 'likes'

class Task(BaseModel):
    task_id: str
    author: str
    count: int

class TopTasksResponse(BaseModel):
    task: List[Task]

class TopUsersRequest(BaseModel):
    pass

class User(BaseModel):
    login: str
    total_likes: int

class TopUsersResponse(BaseModel):
    user: List[User]