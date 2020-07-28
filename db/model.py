from sqlalchemy import Column, Text, Integer, String

from db.base import Base, BaseMixin


class Card(Base, BaseMixin):
    __tablename__ = "cards"
    id = Column(Integer, primary_key=True)
    uid = Column(Integer, primary_key=True)
    known = Column(Integer, default=-1)
    tp = Column(Integer, default=-1)
    front = Column(Text, default="")
    back = Column(Text, default="")


class User(Base, BaseMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, default="")
    password = Column(String, default="")
