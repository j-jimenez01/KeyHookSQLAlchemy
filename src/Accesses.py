from sqlalchemy import Column, Integer, Identity, Float, \
    String, UniqueConstraint, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from orm_base import Base

class Accesses(Base):
    __tablename__ = "accesses"
    door_name = Column('door_name', String(50),  # ForeignKey('doors.door_name'),
                       nullable=False, primary_key=True)
    room_number = Column('room_number', Integer,  # ForeignKey('rooms.room_number'),
                         nullable=False, primary_key=True)
    building_name = Column('building_name', String(50), nullable=False, primary_key=True)

    hook_number = Column('hook_number', Integer, ForeignKey('hooks.hook_number'), nullable=False, primary_key=True)

    __table_args__ = (ForeignKeyConstraint(['door_name', 'room_number', 'building_name'],
                                           ['doors.door_name', 'doors.room_number', 'doors.building_name'],
                                           name="fk_hook_doors_doors_01"),)
    hooks = relationship("Hooks", back_populates='doors_list')

    doors = relationship("Doors", back_populates='hooks_list')

    def __init__(self, hook, door):
        self.hook = hook.hook_number
        self.door = door.door_name

        self.door = door
        self.hook = hook

    def __str__(self):
        return str("Door Name: " + str(self.door_name) + "     Room Number: " + str(self.room_number) +
                   "     Building Name: " + str(self.building_name) + "     Hook Number: " + str(self.hook_number))