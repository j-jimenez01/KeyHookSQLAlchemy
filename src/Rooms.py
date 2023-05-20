from sqlalchemy import Column, Integer, Identity, Float, \
    String, UniqueConstraint, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import relationship

from orm_base import Base
from Building import Buildings

class Rooms(Base):
    __tablename__ = "rooms"
    #fk recieved
    building_name = Column('building_name', String(50), ForeignKey('buildings.building_name'),
                           nullable = False, primary_key=True)
    #attributes in current class
    room_number = Column('room_number',Integer,nullable = False,primary_key=True)
    #door attribute?

    buildings = relationship("Buildings", back_populates="rooms", viewonly=False)
    doors = relationship("Doors", back_populates="rooms", viewonly=False)
    requests = relationship("Requests", back_populates="rooms", viewonly=False)

    def __init__(self, room_number: Integer, building):
        self.room_number = room_number
        self.building_name = building.building_name

    def __str__(self):
        return str("Room Number: " + str(self.room_number) + "     Building Name: " + str(self.building_name))

