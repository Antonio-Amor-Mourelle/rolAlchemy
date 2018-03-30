from flask import Flask, request, json

#import json

# coding=utf-8

# 1 - imports
from base import Session, engine, Base

from models import Material, Recipe, Re_MatAssociation, BagMaterials, Alchemist
from sqlalchemy.exc import IntegrityError

# 2 - generate database schema
Base.metadata.create_all(engine)

# 3 - create a new session
session = Session()





app = Flask(__name__)

################################################################################
                                   #Alchemist#


@app.route('/alchemist/<int:alId>', methods=['GET'])
def alchemist_get(alId):


    al=session.query(Alchemist).filter(Alchemist.id==alId).first()
    ks=al.__table__.columns.keys()
    d={}
    for k in ks:
        if k != 'alId': # No queremos que nos devuelva el id, ya lo sabemos, ha sido el parametro de busqueda
            d[k]=getattr(al,k)
    return json.dumps(d)


@app.route('/alchemist/<int:alId>', methods=['POST'])
def alchemist_post(alId):
    al=session.query(Alchemist).filter(Alchemist.id==alId).first()

    data=request.get_json(force=True, silent=True)#data es un dict
    #data=request.get_json(force=True)
    for k in data.keys():
        if k != "id" and hasattr(al,k): 
            setattr(al,k,data[k])
    return ''   #need to return something, why???



################################################################################
                                   #Material#
@app.route('/material/<int:matId>', methods=['GET'])
def material_get(matId):


    mat=session.query(Material).filter(Material.id==matId).first()
    ks=mat.__table__.columns.keys()
    d={}
    for k in ks:
        if k != 'alId': 
            d[k]=getattr(mat,k)
    return json.dumps(d)


@app.route('/material/<int:matId>', methods=['POST'])
def material_post(matId):
    mat=session.query(Material).filter(Material.id==matId).first()

    data=request.get_json(force=True, silent=True)
    for k in data.keys():
        if k != "id" and hasattr(al,k):
            setattr(al,k,data[k])
    return '' 


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def material_url(pointer):
    pointer=str(pointer)
    if pointer.isdigit():
        return '/material/' + pointer
    else:
        rep=session.query(Material).filter(Material.name==pointer).first()
        return '/material/' + str(rep.id)

################################################################################
                                   #Recipe#

@app.route('/recipe/<int:repId>', methods=['GET'])
def repice_get(repId):


    rep=session.query(Recipe).filter(Recipe.id==repId).first()
    ks=rep.__table__.columns.keys()
    d={}
    for k in ks:
        if k != 'alId': 
            d[k]=getattr(rep,k)
    return json.dumps(d)


@app.route('/recipe/<int:repId>', methods=['POST'])
def recipe_post(repId):
    rep=session.query(Recipe).filter(Recipe.id==repId).first()

    data=request.get_json(force=True, silent=True)
    for k in data.keys():
        if k != "id" and hasattr(al,k):
            setattr(al,k,data[k])
    return ''

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def recipe_url(pointer):
    pointer=str(pointer)
    if pointer.isdigit():
        return '/recipe/' + pointer
    else:
        rep=session.query(Recipe).filter(Recipe.name==pointer).first()
        return '/recipe/' + str(rep.id)

################################################################################
                                   #BagMaterials#

@app.route('/bagmaterials/<int:alId>', methods=['GET'])
def bagmaterials_get(alId):


    '''Esta funcion no devuelve un dict generado de manera generica sino que lo genero
    con el formato concreto que busco: Nombre material, Unidades, URL de la material'''
    bms=session.query(BagMaterials).filter((BagMaterials.alId==alId)).all()
    D={}
    L=[]
    for bm in bms:
        d={}
        #conseguimos el nombre del material
        d['mat']=session.query(Material).filter((Material.id==bm.matId)).first().name
        d['num']=bm.num
        d['url']=material_url(bm.matId)
        L.append(d)
    D['materiales']=L
    return json.dumps(D)

'''
@app.route('/bagmaterials/<int:bmId>', methods=['POST'])
def bagmaterials_post(alId):
    bms=session.query(BagMaterials).filter((BagMaterials.alId==alId)).all()

    data=request.get_json(force=True, silent=True)#data es un dict
    for k in data.keys():
        if k != "id" and hasattr(al,k):
            setattr(al,k,data[k])
    return ''
'''

#quitar esto


################################################################################

if __name__=='__main__':
    app.run(debug=True)
