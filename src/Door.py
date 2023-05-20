from sqlalchemy import Column, Integer, Identity, Float, \
    String, UniqueConstraint, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import relationship

from orm_base import Base
from Rooms import Rooms
from DoorName import DoorNames
from Accesses import Accesses

class Doors(Base):
    __tablename__ = "doors"
    door_name = Column('door_name', String(50), ForeignKey('door_names.door_name'),
                       nullable=False, primary_key=True)
    room_number = Column('room_number', Integer,  # ForeignKey('rooms.room_number'),
                         nullable=False, primary_key=True)
    building_name = Column('building_name', String(50),  # ForeignKey('rooms.building_name'),
                           nullable=False, primary_key=True)
    __table_args__ = (ForeignKeyConstraint(['room_number', 'building_name'], ['rooms.room_number', 'rooms.building_name'],
                         name="fk_doors_rooms_01"),)

    doornames = relationship("DoorNames", back_populates="doors", viewonly=False)

    rooms = relationship("Rooms", back_populates="doors", viewonly=False)

    hooks_list: [Accesses] = relationship("Accesses", back_populates="doors", viewonly=False)

    # Constructor
    def __init__(self, door_name, room):
        self.door_name = door_name.door_name
        self.room_number = room.room_number
        self.building_name = room.building_name
        self.hooks_list = []

    def __str__(self):
        return str("Door Name: "+ str(self.door_name) +"     Room Number: " + str(self.room_number) +
                   "     Building Name: " + str(self.building_name))
    #edit this but use for now to get code running
    def add_hook(self, hook):
        for next_hook in self.hooks_list:
            if next_hook == hook:
                print("Hook already exist.")
                return
        hook_door = Accesses(hook, self)
        hook.add_door(hook_door)
        self.hooks_list.append(hook_door)


