
from sqlalchemy import Column, String, Integer, Table, ForeignKey

from base import Base


class BagRecipes(Base):
    __tablename__ = 'BagRecipes'

    id = Column(Integer,ForeignKey('recipes.id'), primary_key=True)
    num = Column(Integer)

    def __init__(self, id, num):
        self.id = id
        self.num = num
