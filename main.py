# coding=utf-8

# 1 - imports
from base import Session, engine, Base
#from material import Material
#from recipe import Recipe, Re_MatAssociation
#from bagMaterials import BagMaterials
#from bagPotions import BagPotions
#from alchemist import Alchemist

from models import Material, Recipe, Re_MatAssociation, BagMaterials, Alchemist

from sqlalchemy.exc import IntegrityError

# 2 - generate database schema
Base.metadata.create_all(engine)

# 3 - create a new session
session = Session()


def flush_input():
    try:
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    except ImportError:
        import sys, termios
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)


################ MATERIALS #######################
def getMaterial(pointer):
    if isinstance(pointer, Material):
        return pointer
    if pointer.isdigit():
        return session.query(Material).filter(Material.id==int(pointer)).first()
    else:
        return session.query(Material).filter(Material.name==pointer).first()

def MaterialDesc(pointer):
    mat=getMaterial(pointer)
    print(mat.name + ':' + '\n\t'+ mat.desc)

def listMaterials():
    materials = session.query(Material).all()

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
    if isinstance(pointer, Material):
        return pointer
    if pointer.isdigit():
        return session.query(Recipe).filter(Recipe.id==int(pointer)).first()
    else:
        return session.query(Recipe).filter(Recipe.name==pointer).first()


def getRecipeMaterials(pointer):
    '''Consigue los materiales presentes en una receta y su numero'''
    re=getRecipe(pointer)
    mats={}
    for r_mAsoc in re.materials:
        mats[r_mAsoc.material]=r_mAsoc.num_material
    return mats

def RecipeDesc(pointer):
    re=getRecipe(pointer)
    print(re.name + ':')
    print(re.materials)# En realidad es una lista de asociaciones r-mAsoc
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
    #conseguimos los materiales que conforman la receta
    listMaterials()
    res=input('Selecciona separando por "," los materiales de la receta\n \
    Ejemplo: azufre x 2, acido x 1, 2(<--tbn indexa por id) x 3\n  ')
    #lista de "punteros(nombres o ids) a los materiales"
    lMatPointers= res.split(',')
    #conseguimos los materiales
    lR_MAsocs=[]
    for pointer in lMatPointers:
            pointer,num=pointer.split(' x ')
            print(pointer,num)
            mat=getMaterial(pointer)
            lR_MAsocs.append(Re_MatAssociation(mat,num))


    r=Recipe(name, desc, lR_MAsocs)
    m=Material(name,desc)


    #añadimos la receta a la base de datos(no hasta el commit)
    session.add(m)
    session.add(r)
    try:
        session.commit()
    #es en el commit donde puede dar errores de integridad
    except IntegrityError:
        session.rollback()
        print('Ha habido un problema con la nueva receta')

################ BAG ############################
#----------Materials----------#
def getBagMaterial(al,mat):
    al=getAlchemist(al)
    mat=getMaterial(mat)
    return session.query(BagMaterials).filter(BagMaterials.alId==al.id,BagMaterials.matId==mat.id).first()

def getBagMaterials(al):
    '''devuelve un diccionario con los materiales y su cantidad'''
    al=getAlchemist(al)
    bms=session.query(BagMaterials).filter(BagMaterials.alId==al.id).all()
    mats={}
    for bm in bms:
        mats[getMaterial(str(bm.matId))]=bm.num
    return mats


def listBagMaterials(al):
    '''imprime por pantalla los materiales en la mochila y su numero'''
    al=getAlchemist(al)
    bms = session.query(BagMaterials).filter(BagMaterials.alId==al.id)

    print('\nMis Materiales:')
    for bm in bms:
        mat=getMaterial(str(bm.matId))
        print('\t'+str(bm.matId)+'· '+mat.name+ ' x ' + str(bm.num))
    print('')


def addMaterialToBag(al, mat, num):

    al=getAlchemist(al)
    mat=getMaterial(mat)
    num=int(num)
    try:
        bm=session.query(BagMaterials).filter(BagMaterials.alId==al.id,BagMaterials.matId==mat.id).first()
        bm.num+=int(num)
        session.commit()
        #print('material actualizado')
    except:
        bm=BagMaterials(al.id,mat.id, num)
        session.add(bm)
        session.commit()
        #print('materials añadido')


def addMaterialToBagInterface(al):
    listMaterials()
    mat=input('¿Que material queres añadir a la mochila? ')
    num=input('¿cuantos quieres añadir a la mochila? ')
    addMaterialToBag(al,mat,num)



#----------Potions----------#
def checkDoPotion(al, pointer):
    '''comprueba si es posible realizar una pocion'''
    alMats=getBagMaterials(al)
    potMats=getRecipeMaterials(pointer)
    keys=potMats.keys()

    try:
        for key in keys:
            alNum=alMats[key]
            potNum=potMats[key]
            if alNum<potNum:
                return False
    except:
        return False
    return True


def doPotion(al, pointer):
    '''comprueba q se pueda hacer la pocion,
       elimina los materiales correspondientes
       y devuelve la pocion'''
    if not checkDoPotion(al, pointer):
        return

    potMats=getRecipeMaterials(pointer)
    keys=potMats.keys()

    for key in keys:
        addMaterialToBag(al,key,potMats[key]*-1)

    addMaterialToBag(al,pointer,1)

'''
def listBagPotions(al):
    al=getAlchemist(al)
    bps = session.query(BagPotions).filter(BagPotions.alId==al.id)
    print('\nMis Pociones:')
    for bp in bps:
        pot=getRecipe(str(bp.potId))
        print('\t'+str(bp.potId)+'· '+pot.name+ ' x ' + str(bp.num))
    print('')
'''


def addPotionsToBag(al, pointer,num):
    al=getAlchemist(al)
    num=int(num)

    for i in range(num):
        doPotion(al, pointer)



def addPotionsToBagInterface(al):

    print(getAlchemistRecipes(al))
    al=getAlchemist(al)
    pointer=input('¿Que pocion queres añadir a la mochila? ')
    num=input('¿Cuantos quieres añadir a la mochila? ')

    addPotionsToBag(al,pointer,num)



################ ALCHEMIST ############################
def getAlchemist(pointer):
    if isinstance(pointer, Alchemist):
        return pointer
    if pointer.isdigit():
        return session.query(Alchemist).filter(Alchemist.id==int(pointer)).first()
    else:
        return session.query(Alchemist).filter(Alchemist.name==pointer).first()

def getAlchemistRecipes(pointer):
    return getAlchemist(pointer).recipes


def listAlchemists():
    alchemists = session.query(Alchemist).all()

    print('\nAlchemist activos:')
    for al in alchemists:
        print('\t'+str(al.id)+'· '+al.name)
    print('')

################ MAIN ############################

al=input("¿Quien eres?")
al=getAlchemist(al)
print('\n')
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
                        \n\t9·  Añadir pociones a la mochila\
                        \n\t10· Añadir recetas a mi libro de recetas\
                        \n\t11· Ver la mochila\
                        \n-->')


    if res=='0':
        session.close()
        break

    elif res=='1':
        addMaterial()

    elif res=='2':
        listMaterials()

    elif res=='3':
        listMaterials()
        res=input('¿Que material queres ver en detalle? ')
        try:
            MaterialDesc(res)
        except:
            print("Error buscando material")

    elif res=='4':
        addRecipe()

    elif res=='5':
        listRecipes()

    elif res=='6':
        listRecipes()
        res=input('¿Que receta queres ver en detalle? ')
        try:
            RecipeDesc(res)
        except:
            print("Error buscando receta")

    elif res=='7':
        listAlchemists()

    elif res=='8':
        addMaterialToBagInterface(al)

    elif res=='9':
        addPotionsToBagInterface(al)

    elif res=='10':
        print(getAlchemistRecipes(al))

    elif res=='11':
        listBagMaterials(al)
        #listBagPotions(al)

#hola
    flush_input()   #para vaciar le buffer de input 
