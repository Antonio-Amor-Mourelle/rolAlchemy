
from sqlalchemy import Column, String, Integer, Table, ForeignKey

from sqlalchemy.orm import relationship

from base import Base


alchemist_recipes_association = Table('alchemists_recipes', Base.metadata,
    Column('alchemist_id', Integer, ForeignKey('alchemists.id'), primary_key=True),
    Column('recipes_id', Integer, ForeignKey('recipes.id'), primary_key=True)    
)

class Alchemist(Base):
    __tablename__ = 'alchemists'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    recipes = relationship("Recipe", secondary=alchemist_recipes_association)

    def __init__(self, name, l=[]):
        self.name = name
        self.recipes=l
