
from sqlalchemy import Column, String, Integer, Table, ForeignKey

from base import Base


class BagPotions(Base):
    __tablename__ = 'bagPotions'

    alId = Column(Integer,ForeignKey('alchemists.id'), primary_key=True)
    potId = Column(Integer,ForeignKey('recipes.id'), primary_key=True)
    num = Column(Integer)

    def __init__(self, alId,potId, num):
        self.alId = alId
        self.potId = potId
        self.num = num
