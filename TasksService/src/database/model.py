from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func, UUID
from sqlalchemy.orm import declarative_base
import uuid

Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4) 
    title = Column(String)
    text = Column(String)
    author = Column(String)
    creation_date = Column(DateTime, default=func.now())  

class StatsTable(Base):
    __tablename__ = "stats_table"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    views_count = Column(Integer)
    likes_count = Column(Integer)

    task_id = Column(UUID(as_uuid=True), ForeignKey('tasks.id'))

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    text = Column(String)
    creation_date = Column(DateTime)

    task_id = Column(UUID(as_uuid=True), ForeignKey('tasks.id'))

    author = Column(String)

    parent_comment_id = Column(Integer, ForeignKey("comments.id"))

class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime)

    user = Column(String)

    task_id = Column(UUID(as_uuid=True), ForeignKey('tasks.id'))

class View(Base):
    __tablename__ = "views"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime)

    user = Column(String)

    task_id = Column(UUID(as_uuid=True), ForeignKey('tasks.id'))
