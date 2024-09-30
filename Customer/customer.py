# Customer/customer.py


from sqlalchemy import Column, Integer, String, Date, TIMESTAMP, Boolean, func
from sqlalchemy.orm import relationship
from db import Base
import hashlib

class Customer(Base):
    __tablename__ = 'customers'

    CustomerID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(255), nullable=False)
    Gender = Column(String(255))
    Birthdate = Column(Date)
    PhoneNumber = Column(String(255))
    Address = Column(String(255))
    Username = Column(String(255))
    Password = Column(String(255))
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

# Function to add a customer
def add_customer(name, gender, birthdate, phone_number, address, username, password, role, created_at):
    new_customer = Customer(
        Name=name,
        Gender=gender,
        Birthdate=birthdate,
        PhoneNumber=phone_number,
        Address=address,
        Username=username,
        Password=hash_password(password),
        role=role,
        created_at=created_at
    )
    session.add(new_customer)
    session.commit()
    print(f"Customer '{name}' added to the database.")

# Function to get a customer by username
def get_customer_by_username(username):
    return session.query(Customer).filter(Customer.Username == username).first()

# Function to get a customer by ID
def get_customer_by_id(customer_id):
    return session.query(Customer).filter(Customer.CustomerID == customer_id).first()

# Function to get all customers
def get_all_customers():
    return session.query(Customer).all()

def attempt_login(username, password):
    customer = get_customer_by_username(username)
    if customer is None:
        print("Customer not found.")
        return False
    if customer.Password == hash_password(password):
        return True
    return False

def hash_password(password):
    # Use hashlib with SHA-256 to hash the password
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password

def get_PizzasOrderedCount(customerID):
    customer = session.query(Customer).filter(Customer.CustomerID == customerID).first()
    return customer.PizzasOrderedCount

def add_PizzasOrderedCount(customerID, amount):
    customer = session.query(Customer).filter(Customer.CustomerID == customerID).first()
    customer.PizzasOrderedCount += amount
    session.commit()
    print(f"PizzasOrderedCount for CustomerID '{customerID}' updated to '{customer.PizzasOrderedCount}'.")

def get_postal_code(customerID):
    customer = session.query(Customer).filter(Customer.CustomerID == customerID).first()
    return customer.Address