
from sqlalchemy import Column, String, Integer, Table, ForeignKey

from base import Base


class BagMaterials(Base):
    __tablename__ = 'bagMaterials'

    alId = Column(Integer,ForeignKey('alchemists.id'), primary_key=True)
    matId = Column(Integer,ForeignKey('materials.id'), primary_key=True)
    num = Column(Integer)

    def __init__(self, alId,matId, num):
        self.alId = alId
        self.matId = matId
        self.num = num
