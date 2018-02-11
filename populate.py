# coding=utf-8

# 1 - imports
from base import Session, engine, Base
from material import Material
from recipe import Recipe
from bagMaterials import BagMaterials
from bagRecipes import BagRecipes
from alchemist import Alchemist

from sqlalchemy.exc import IntegrityError

# 2 - generate database schema
Base.metadata.create_all(engine)

# 3 - create a new session
session = Session()

# 4 - create materials
azufre = Material("azufre", 'Esto es azufre')
sal = Material("sal", 'Esto es sal')
acido = Material("acido", 'Esto es acido')

session.add(azufre)
session.add(sal)
session.add(acido)

session.commit()
print('material commit ok')

#5 - creates recipes
r1 = Recipe("receta 1", "Esta es la receta 1")
r2 = Recipe("receta 2", "Esta es la receta 1")
r3 = Recipe("receta 3", "Esta es la receta 1")

r1.materials = [azufre]
r2.materials = [sal]
r3.materials = [sal,sal, acido]

session.commit()
print('recipes commit ok')


# ** - add alchemists
al1= Alchemist('ton')
al1.recipes=[r1,r3]

session.add(al1)

session.commit()
print('alchemist commit ok')

'''
# 7 - add materials to bag
bm1 = BagMaterials(azufre.id, 2)
# 8 - add recipes to bag
br1 = BagRecipes(r1.id, 1)
br2 = BagRecipes(r2.id, 3)

session.add(bm1)

session.add(br1)
session.add(br2)

session.commit()
'''
session.close()
