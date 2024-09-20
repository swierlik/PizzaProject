from sqlalchemy import Column, Integer, String, Date, TIMESTAMP
from db import Base, session

class Customer(Base):
    __tablename__ = 'Customer'

    CustomerID = Column(Integer, primary_key=True)
    Name = Column(String(255), nullable=False)
    Gender = Column(String(255), nullable=True)
    Birthdate = Column(Date, nullable=True)
    PhoneNumber = Column(String(255), nullable=True)
    Address = Column(String(255), nullable=True)
    Username = Column(String(255), nullable=False, unique=True)
    Password = Column(String(255), nullable=False)
    PizzasOrderedCount = Column(Integer, default=0)
    role = Column(String(255), nullable=False, default="customer")
    created_at = Column(TIMESTAMP, nullable=False)

    def __repr__(self):
        return (f"<Customer(CustomerID={self.CustomerID}, Name='{self.Name}', Gender='{self.Gender}', "
                f"Birthdate={self.Birthdate}, PhoneNumber='{self.PhoneNumber}', Address='{self.Address}', "
                f"Username='{self.Username}', PizzasOrderedCount={self.PizzasOrderedCount}, role='{self.role}', "
                f"created_at={self.created_at})>")

# Function to add a customer
def add_customer(name, gender, birthdate, phone_number, address, username, password, role, created_at):
    new_customer = Customer(
        Name=name,
        Gender=gender,
        Birthdate=birthdate,
        PhoneNumber=phone_number,
        Address=address,
        Username=username,
        Password=password,
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
