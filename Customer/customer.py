# Customer/customer.py

from sqlalchemy import Column, Integer, String, Date, TIMESTAMP, Boolean, func
from sqlalchemy.orm import relationship
from db import Base
import hashlib

class Customer(Base):
    __tablename__ = 'customers'

    CustomerID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(255), nullable=False)
    Gender = Column(String(255), nullable=True)
    Birthdate = Column(Date, nullable=True)
    PhoneNumber = Column(String(255), nullable=True)
    Address = Column(String(255), nullable=True)
    Username = Column(String(255), unique=True, nullable=False)
    Password = Column(String(255), nullable=False)
    PizzasOrderedCount = Column(Integer, default=0)
    role = Column(String(255), default='customer')
    created_at = Column(TIMESTAMP, server_default=func.now())

    # Relationships
    orders = relationship('Order', back_populates='customer')

    def __repr__(self):
        return f"<Customer(CustomerID={self.CustomerID}, Name='{self.Name}')>"

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password):
        hashed_input_password = self.hash_password(password)
        return self.Password == hashed_input_password

    @classmethod
    def add_customer(cls, session, name, username, password, **kwargs):
        # Hash the password
        hashed_password = cls.hash_password(password)
        # Create a new Customer instance
        new_customer = cls(
            Name=name,
            Username=username,
            Password=hashed_password,
            **kwargs
        )
        # Add to the session
        session.add(new_customer)
        # Do not commit here; let the calling code handle it
        return new_customer

# Existing functions (if needed)
def get_customer_by_username(username):
    from db import SessionLocal
    session = SessionLocal()
    customer = session.query(Customer).filter(Customer.Username == username).first()
    session.close()
    return customer

def get_customer_by_id(customer_id):
    from db import SessionLocal
    session = SessionLocal()
    customer = session.query(Customer).filter(Customer.CustomerID == customer_id).first()
    session.close()
    return customer

def get_all_customers():
    from db import SessionLocal
    session = SessionLocal()
    customers = session.query(Customer).all()
    session.close()
    return customers
