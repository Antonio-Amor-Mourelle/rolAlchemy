
from sqlalchemy import Column, String, Integer, Table, ForeignKey

from sqlalchemy.orm import relationship

from base import Base


class Re_MatAssociation(Base):
    '''Esta clase permite tener una relacion N-N
       entre Recipes y Materiales aportando el numero
       de materiales como info extra'''

    __tablename__ = 'recipes_materials'
    recipe_id = Column(Integer, ForeignKey('recipes.id'), primary_key=True)
    material_id = Column(Integer, ForeignKey('materials.id'), primary_key=True)
    material = relationship("Material")
    num_material = Column(Integer)

    def __init__(self,mat, numMat=1):
        self.material=mat
        self.num_material=numMat

    def __repr__(self):
        return str(self.material)+' x '+ str(self.num_material)


class Recipe(Base):
    __tablename__ = 'recipes'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    desc = Column(String(200))
    materials = relationship("Re_MatAssociation")

    def __init__(self, name, desc,l=[]):
        self.name = name
        self.desc = desc
        self.materials=l
    def __repr__(self):
        return self.name
