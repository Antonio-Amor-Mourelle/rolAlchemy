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
        d[k]=getattr(al,k)
    return json.dumps(d)


@app.route('/alchemist/<int:alId>', methods=['POST'])
def alchemist_post(alId):
    al=session.query(Alchemist).filter(Alchemist.id==alId).first()

    data=request.get_json(force=True, silent=True)#data es un dict
    #data=request.get_json(force=True)
    for k in data.keys():
        if k != "id" and hasattr(al,k): # no deberia ser necesario el hasattr pero lo ponemos por si acaso
            print('aqui')
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



################################################################################
                                   #Recipe#

@app.route('/recipe/<int:repId>', methods=['GET'])
def repice_get(repId):


    rep=session.query(Recipe).filter(Recipe.id==repId).first()
    ks=rep.__table__.columns.keys()
    d={}
    for k in ks:
        d[k]=getattr(rep,k)
    return json.dumps(d)


@app.route('/recipe/<int:repId>', methods=['POST'])
def recipe_post(repId):
    rep=session.query(Recipe).filter(Recipe.id==repId).first()

    data=request.get_json(force=True, silent=True)#data es un dict
    for k in data.keys():
        if k != "id" and hasattr(al,k):
            setattr(al,k,data[k])
    return ''



################################################################################
                                   #BagMaterials#
'''
@app.route('/bagmaterials/<int:alId>', methods=['GET'])
def bagmaterials_get(alId):


    bms=session.query(BagMaterials).filter((BagMaterials.alId==alId)).all()
    ks=bm[0].__table__.columns.keys()
    d={}
    for k in ks:
        d[k]=getattr(bm,k)
    return json.dumps(d)


@app.route('/bagmaterials/<int:bmId>', methods=['POST'])
def bagmaterials_post(alId):
    bms=session.query(BagMaterials).filter((BagMaterials.alId==alId)).all()

    data=request.get_json(force=True, silent=True)#data es un dict
    for k in data.keys():
        if k != "id" and hasattr(al,k):
            setattr(al,k,data[k])
    return ''
'''


################################################################################

if __name__=='__main__':
    app.run(debug=True)
