from sqlalchemy import Column, String, Integer, Table, ForeignKey

from sqlalchemy.orm import relationship

from base import Base




####################     Material     ############################
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



####################     Recipe     ############################
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



 
####################     BagMaterial     ############################
class BagMaterials(Base):
    __tablename__ = 'bagMaterials'

    alId = Column(Integer,ForeignKey('alchemists.id'), primary_key=True)
    matId = Column(Integer,ForeignKey('materials.id'), primary_key=True)
    num = Column(Integer)

    def __init__(self, alId,matId, num):
        self.alId = alId
        self.matId = matId
        self.num = num



 
####################     Alchemist     ############################
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
