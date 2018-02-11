# coding=utf-8

#AWESOME SQLALCHEMY TUTORIAL 
#https://auth0.com/blog/sqlalchemy-orm-tutorial-for-python-developers/


from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://alumnodb:alumnodb@localhost:5432/rol-alquemy')
Session = sessionmaker(bind=engine)


Base = declarative_base()
