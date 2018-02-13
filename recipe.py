
from sqlalchemy import Column, String, Integer, Table, ForeignKey

from sqlalchemy.orm import relationship

from base import Base


recipes_materials_association = Table('recipes_materials', Base.metadata,
    Column('recipe_id', Integer, ForeignKey('recipes.id')),
    Column('material_id', Integer, ForeignKey('materials.id'))
)

class Recipe(Base):
    __tablename__ = 'recipes'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    desc = Column(String(200))
    materials = relationship("Material", secondary=recipes_materials_association)

    def __init__(self, name, desc,l=[]):
        self.name = name
        self.desc = desc
        self.materials=l
    def __repr__(self):
        return self.name
