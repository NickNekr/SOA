from sqlalchemy import (
    Column,
    Integer,
    String,
    UUID
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class LikesStats(Base):
    __tablename__ = "LikesStats"
    __table_args__ = {"comment": "Таблица, хранящая статистику по лайкам"}

    id = Column(Integer, primary_key=True)
    task_id = Column(UUID(as_uuid=True), unique=True)
    count = Column(Integer, default=0)

class ViewsStats(Base):
    __tablename__ = "ViewsStats"
    __table_args__ = {"comment": "Таблица, хранящая статистику по просмотрам"}

    id = Column(Integer, primary_key=True)
    task_id = Column(UUID(as_uuid=True), unique=True)
    count = Column(Integer, default=0)

class Likes(Base):
    __tablename__ = "Like"
    __table_args__ = {"comment": "Таблица, хранящая лайки"}

    id = Column(Integer, primary_key=True)
    task_id = Column(UUID(as_uuid=True))
    username = Column(String(50), nullable=False)

class Views(Base):
    __tablename__ = "View"
    __table_args__ = {"comment": "Таблица, хранящая просмотры"}

    id = Column(Integer, primary_key=True)
    task_id = Column(UUID(as_uuid=True))
    username = Column(String(50), nullable=False)

class TaskToAuthor(Base):
    __tablename__ = "TaskToAuthor"
    __table_args__ = {"comment": "Таблица, хранящая соотнесение задачи к автору"}

    id = Column(Integer, primary_key=True)
    task_id = Column(UUID(as_uuid=True))
    author = Column(String(50), nullable=False)
