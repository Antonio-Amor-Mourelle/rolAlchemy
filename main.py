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


################ MATERIALS #######################
def getMaterial(pointer):
    if pointer.isdigit():
        return session.query(Material).filter(Material.id==int(pointer)).first()
    else:
        return session.query(Material).filter(Material.name==pointer).first()

def MaterialDesc(pointer):
    mat=getMaterial(pointer)
    print(mat.name + ':' + '\n\t'+ mat.desc)

def listMaterials():
    materials = session.query(Material).all()

    # 4 - print movies' details
    print('\nMateriales disponibles:')
    for mat in materials:
        print('\t'+str(mat.id)+'· '+mat.name)
    print('')


def addMaterial():
    res=input('Introduce: nombre " || " descripcion ,del nuevo material\n')
    try:
        name, desc= res.split(' || ', maxsplit=1)
    except ValueError:
        print('ERRROR: Introduce una cadena separada por " || " sin comillas')
        return
    #creamos el nuevo material
    m= Material(name, desc)
    session.add(m)
    try:
        session.commit()
    #es en el commit donde puede sar errores de integridad
    except IntegrityError:
        session.rollback()
        print('Material ya existente')



################ RECIPES #########################
def getRecipe(pointer):
    if pointer.isdigit():
        return session.query(Recipe).filter(Recipe.id==int(pointer)).first()
    else:
        return session.query(Recipe).filter(Recipe.name==pointer).first()


def RecipeDesc(pointer):
    re=getRecipe(pointer)
    print(re.name + ':')
    print(re.materials)
    print(re.desc)


def listRecipes():
    recipes = session.query(Recipe).all()

    # 4 - print movies' details
    print('\nRecetas disponibles:')

    for re in recipes:
        print('\t'+str(re.id)+'· '+re.name)
    print('')


def addRecipe():
    res=input('Introduce: nombre " || " descripcion ,de la nueva receta\n')
    try:
        name, desc= res.split(' || ', maxsplit=1)
    except ValueError:
        print('Introduce una cadena separada por " || " sin comillas')
        return
    r=Recipe(name, desc)

    #conseguimos los materiales que conforman la receta
    listMaterials()
    res=input('Selecciona separando por "," los materiales de la receta: ')
    #lista de "punteros(nombres o ids) a los materiales"
    lMatPointers= res.split(',')
    #conseguimos los materiales
    lmats=[]
    for pointer in lMatPointers:
            lmats.append(getMaterial(pointer))
    #añadimos los materiales a la receta
    r.materials=lmats
    #añadimos la receta a la base de datos(no hasta el commit)
    session.add(r)

    try:
        session.commit()
    #es en el commit donde puede sar errores de integridad
    except IntegrityError:
        session.rollback()
        print('Ha habido un problema con la nueva receta')

################ BAG ############################
def addMaterialToBag():
    listMaterials()
    mat=input('¿Que material queres añadir a la mochila? ')
    num=input('¿cuantos quieres añadir a la mochila? ')
    mat=getMaterial(mat)

    print('añadiendo '+ mat.name + ' con id: '+ str(mat.id))
    bm = BagMaterials(mat.id, num)
    session.add(bm)
    try:
        session.commit()
        print('añadido')
    except:
        print('ha ocurrido algun error')

def addPotionsToBag():
    pass

################ ALCHEMIST ############################
def getAlchemist(pointer):
    if pointer.isdigit():
        return session.query(Alchemist).filter(Alchemist.id==int(pointer)).first()
    else:
        return session.query(Alchemist).filter(Alchemist.name==pointer).first()


def listAlchemists():
    alchemists = session.query(Alchemist).all()

    # 4 - print movies' details
    print('\nAlchemist activos:')
    for al in alchemists:
        print('\t'+str(al.id)+'· '+al.name)
    print('')

################ MAIN ############################
while True:
    res=input('----------¿Que quieres hacer?---------- \
                        \n\t0· EXIT\
                        \n\t------GM------\
                        \n\t1·  Añadir nuevo Material \
                        \n\t2·  Listar Materiales \
                        \n\t3·  Detalles Material \
                        \n\t4·  Añadir nueva Receta \
                        \n\t5·  Listar Recetas(GAME) \
                        \n\t6·  Detalles Receta \
                        \n\t7·  Listar Alquimistas \
                        \n\t------PLAYER------\
                        \n\t8·  Añadir materiales a la mochila \
                        \n\t9·  Añadir recetas a mi libro de recetas\
                        \n\t10· Ver la mochila\
                        \n-->')


    if res=='0':
        session.close()
        break

    if res=='1':
        addMaterial()

    if res=='2':
        listMaterials()

    if res=='3':
        listMaterials()
        res=input('¿Que material queres ver en detalle? ')
        MaterialDesc(res)

    if res=='4':
        addRecipe()

    if res=='5':
        listRecipes()

    if res=='6':
        listRecipes()
        res=input('¿Que receta queres ver en detalle? ')
        RecipeDesc(res)

    if res=='7':
        listAlchemists()

    if res=='8':
        addMaterialToBag()

    if res=='9':
        res=input('¿Quien eres? ')
        res=getAlchemist(res)
        print(res.recipes)


    if res=='10':
        print('POR IMPLEMENTAR')
