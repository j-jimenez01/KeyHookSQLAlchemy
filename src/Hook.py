from sqlalchemy import Column, Integer, Identity, Float, \
    String, UniqueConstraint, Sequence
from sqlalchemy.orm import relationship
from orm_base import Base

from Accesses import Accesses

class Hooks(Base):
    __tablename__ = "hooks"
    hook_number = Column('hook_number', Integer, Identity("hook_seq", start=1),
                        nullable=False, primary_key=True)

    doors_list: [Accesses] = relationship("Accesses", back_populates="hooks")

    keys = relationship("Keys", back_populates="hooks")

    def __init__(self):
        pass

    def add_door(self, door):
        for next_door in self.doors_list:
            if next_door == door:
                print("Door already exist.")
                return
        hook_door = Accesses(self, door)
        door.hooks_list.append(hook_door)
        self.doors_list.append(hook_door)

    def __str__(self):
        return str("Hook Number: " + str(self.hook_number))  # maybe might be only hook number