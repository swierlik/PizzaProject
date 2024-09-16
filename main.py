# main.py
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from models import *
from db_setup import setup_database

def main():
    engine = setup_database()
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Example of querying data
    customers = session.query(Customer).all()
    for customer in customers:
        print(f"Customer ID: {customer.CustomerID}, Name: {customer.Name}")
    
    # Example of adding a new record
    new_customer = Customer(
        Name='John Doe',
        Gender='Male',
        Birthdate=datetime(1990, 5, 14),
        PhoneNumber='555-1234',
        Address='123 Main St',
        Username='johndoe',
        Password='securepassword',
        PizzasOrderedCount=0,
        role='Customer',
        created_at=datetime.now()
    )
    session.add(new_customer)
    session.commit()
    
    print("New customer added.")

if __name__ == "__main__":
    main()
