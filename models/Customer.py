# Customers/Customer.py
from sqlalchemy import Boolean, Column, Integer, String, Date, TIMESTAMP, func
from sqlalchemy.orm import relationship
from database import Base

class Customer(Base):
    __tablename__ = 'customers'  # Use lowercase for table name

    CustomerID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(255), nullable=True)
    Gender = Column(String(255), nullable=True)
    Birthdate = Column(Date, nullable=True)
    PhoneNumber = Column(String(255), nullable=True)
    Address = Column(String(255), nullable=True)
    PostalCode = Column(String(255), nullable=True)
    Username = Column(String(255), unique=True, nullable=False)
    Password = Column(String(255), nullable=False)
    PizzasOrderedCount = Column(Integer, default=0)
    CreatedAt = Column(TIMESTAMP, server_default=func.now())
    IsNext10Discount = Column(Boolean, default=False)

    # Relationships
    orders = relationship('Order', back_populates='customer')

    def __repr__(self):
        return f"<Customer(CustomerID={self.CustomerID}, Name='{self.Name}')>"
