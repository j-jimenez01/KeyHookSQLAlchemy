from sqlalchemy import Column, Integer, Identity, Float, \
    String, UniqueConstraint, ForeignKey

from sqlalchemy.orm import relationship

from Request import Requests

from orm_base import Base

class Keys(Base):
    __tablename__ = "keys"
    key_number = Column('key_number', Integer, ForeignKey('hooks.hook_number'),  # nullable=False,
                        primary_key=True)
    key_id = Column('key_id', Integer, Identity("key_id_seq", start=1),
                    nullable=False, primary_key=True)

    hooks = relationship("Hooks", back_populates="keys")
    requests = relationship("Requests", back_populates="keys")

    def __init__(self, original_hook):
        self.key_number = original_hook.hook_number
        self.requests_list = []

    def __str__(self):
        return str("Key Number: " + str(self.key_number) + "     Key ID: " + str(self.key_id))  # might just be key_id


    def add_request(self, request):
        for next_request in self.requests_list:
            if next_request == request:
                print("Request already exist.")
                return
        self.requests_list.append(request)