# new
import datetime

from sqlalchemy import Column, Integer, Identity, Float, \
    String, UniqueConstraint, ForeignKey, DateTime, ForeignKeyConstraint  # new
from sqlalchemy.orm import relationship

from sqlalchemy.sql import func

from orm_base import Base


class LostKeys(Base):
    __tablename__ = "lost_keys"
    request_request_id = Column('request_id', Integer, ForeignKey('requests.request_id'), nullable=False,
                                primary_key=True)
    loaned_out_date = Column('loaned_out_date', DateTime, nullable=False, primary_key=True)
    lost_date = Column('lost_date', DateTime(timezone=False), default=func.now(), nullable=False, primary_key=True)


    requests = relationship("Requests", back_populates="lostkeys")

    # Constructor
    def __init__(self, request, loan_date: DateTime):
        self.request_request_id = request.request_id
        self.loaned_out_date = loan_date
    def __str__(self):
        return str("Request id: "+ str(self.request_request_id) +"     Loaned Out Date: " + str(self.loaned_out_date) +
                   "     Lost Date: " + str(self.loss_date))