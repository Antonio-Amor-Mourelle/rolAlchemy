# coding=utf-8

# 1 - imports
from base import Session, engine, Base
from material import Material
from recipe import Recipe
from bagMaterials import BagMaterials

from sqlalchemy.exc import IntegrityError

# 2 - generate database schema
Base.metadata.create_all(engine)

# 3 - create a new session
session = Session()

def getMaterialByName(name):
    #FALLA
    return session.query(Material).filter(Material.name==name)[0]


def getMaterialById(id):
    return session.query(Material).filter(Material.id==id).first()


mat=getMaterialById(3)

bm1=BagMaterials(mat.id,2)

session.add(bm1)

session.commit()
session.close()
