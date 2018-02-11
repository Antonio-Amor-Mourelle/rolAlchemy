
from sqlalchemy import Column, String, Integer, Table, ForeignKey

from base import Base


class BagMaterials(Base):
    __tablename__ = 'BagMaterials'

    id = Column(Integer,ForeignKey('materials.id'), primary_key=True)
    num = Column(Integer)

    def __init__(self, id, num):
        self.id = id
        self.num = num
