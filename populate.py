# coding=utf-8

# 1 - imports
from base import Session, engine, Base
from material import Material
from recipe import Recipe, Re_MatAssociation
from alchemist import Alchemist
from bagMaterials import BagMaterials
from bagPotions import BagPotions

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
r_m1=Re_MatAssociation(azufre)
r_m2=Re_MatAssociation(sal,1)
r_m2=Re_MatAssociation(acido,3)


r1 = Recipe("receta 1", "Esta es la receta 1",[r_m1,r_m2])
r2 = Recipe("receta 2", "Esta es la receta 2",[r_m1,r_m3])
r3 = Recipe("receta 2", "Esta es la receta 2",[r_m1,r_m2,r_m3])



session.add(r1)
#session.add(r2)
#session.add(r3)

session.commit()
print('recipes commit ok')


# ** - add alchemists
al1= Alchemist('ton',list(set([r1,r3])))
al2= Alchemist('javi',list(set([r2,r3])))

session.add(al1)
session.add(al2)

session.commit()
print('alchemist commit ok')

bm1=BagMaterials(1,1,5)
bm2=BagMaterials(2,3,10)

session.add(bm1)
session.add(bm2)


bp1=BagPotions(1,2,2)
bp2=BagPotions(2,1,5)

session.add(bp2)
session.add(bp2)

session.commit()

print('bag commit ok')

session.close()
