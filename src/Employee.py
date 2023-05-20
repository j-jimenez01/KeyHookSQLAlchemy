from sqlalchemy import Column, Integer, Identity, Float, \
    String, UniqueConstraint
from sqlalchemy.orm import relationship

from orm_base import Base
from Request import Requests

class Employees(Base):
    __tablename__ = "employees"
    employee_id = Column('employee_id', Integer, Identity(start=1, cycle=True),
                         nullable=False, primary_key=True)
    first_name = Column('first_name', String(50), nullable=False)
    last_name = Column('last_name', String(50), nullable=False)

    requests = relationship("Requests", back_populates="employees")

    def __init__(self, first_name: String, last_name: String):
        self.first_name = first_name
        self.last_name = last_name
        self.requests_list = []

    def add_request(self, request):
        for next_request in self.requests_list:
            if next_request == request:
                print("Request already exist.")
                return
        employee_request = Requests(self, request)
        request.employee_list.append(employee_request)
        self.requests_list.append(employee_request)

    def __str__(self):
        return str("Employee ID: " + str(self.employee_id) + "     First Name: " + str(
            self.first_name) + "     Last Name: " + str(self.last_name))