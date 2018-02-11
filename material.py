
from sqlalchemy import Column, String, Integer, Table

from base import Base


class Material(Base):
    __tablename__ = 'materials'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    desc = Column(String(200))


    def __init__(self, name, desc):
        self.name = name
        self.desc = desc
    def __repr__(self):
        return self.name
