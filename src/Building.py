from sqlalchemy import Column, Integer, Identity, Float, \
    String, UniqueConstraint, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from orm_base import Base


class Buildings(Base):
    __tablename__ = "buildings"
    building_name = Column('building_name',String(50),nullable = False, primary_key=True)

    #do this is passing primary key to another class
    # var(class name) = relationship("class name",back_populates="current class")
    rooms = relationship("Rooms",back_populates="buildings",viewonly= False)

    def __init__(self,building_name: String(20)):
        self.building_name = building_name

    def __str__(self):
        return str("Building Name: "+str(self.building_name))
