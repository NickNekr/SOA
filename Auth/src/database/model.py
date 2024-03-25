from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Date,
)
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped

from common.schema import UserSchema, UserDataSchema

Base = declarative_base()

class User(Base):
    __tablename__ = "Users"
    __table_args__ = {"comment": "Таблица, хранящая информацию o пользователях"}

    id = Column(Integer, primary_key=True)

    username = Column(String(50), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

    user_data_id = Column(
        Integer,
        ForeignKey("UsersData.id"),
        nullable=False,
    )

    # user_data: "UserData" = relationship(
    #     "UserData",
    #     lazy='selectin'
    #                          )
    @declared_attr
    def user_data(cls) -> Mapped["UserData"]:
        return relationship("UserData", lazy='selectin')

    def to_pydentic_schema(self):
        return UserSchema(
            first_name=self.user_data.first_name,
            last_name=self.user_data.last_name,
            birth_date=self.user_data.birth_date,
            email=self.user_data.email,
            phone_number=self.user_data.phone_number,
            username=self.username,
            password=self.hashed_password
        )
    
        

class UserData(Base):
    __tablename__ = "UsersData"
    __table_args__ = {"comment": "Таблица, хранящая дополнительную информацию o пользователях"}

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    birth_date = Column(Date)
    email = Column(String, unique=True)
    phone_number = Column(String, unique=True)

    def change_user_data(self, user_data_schema: UserDataSchema):
        self.first_name = user_data_schema.first_name
        self.last_name = user_data_schema.last_name
        self.birth_date = user_data_schema.birth_date
        self.email = user_data_schema.email
        self.phone_number = user_data_schema.phone_number