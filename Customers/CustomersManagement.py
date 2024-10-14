from datetime import datetime
import hashlib

from db import session
from models.Customer import Customer
from models.DiscountCode import DiscountCode
from models.CustomerDiscount import CustomerDiscount

# Function to add a discount code
def add_discount_code(code, description, expiry_date, discount_percentage):
    new_discount_code = DiscountCode(
        Code=code,
        Description=description,
        ExpiryDate=expiry_date,
        DiscountPercentage=discount_percentage
    )
    session.add(new_discount_code)
    session.commit()
    print(f"Discount Code '{code}' added to the database.")

def use_code(code):
    discount_code = session.query(DiscountCode).filter(DiscountCode.Code == code).first()
    if discount_code is None:
        print("Discount code not found.")
        return False
    if discount_code.IsRedeemed:
        print("Discount code has already been redeemed.")
        return False
    if discount_code.ExpiryDate < datetime.now().date():
        print("Discount code has expired.")
        return False
    discount_code.IsRedeemed = True
    session.commit()
    print(f"Discount code '{code}' has been redeemed.")
    return True

def get_discount_by_code(code, price):
    if use_code(code):
        discount_code = session.query(DiscountCode).filter(DiscountCode.Code == code).first()
        return price*(float(discount_code.DiscountPercentage)/100)
    return 0


# Function to add a customer discount
def add_customer_discount(customer_id, discount_code_id):
    new_customer_discount = CustomerDiscount(
        CustomerID=customer_id,
        DiscountCodeID=discount_code_id
    )
    session.add(new_customer_discount)
    session.commit()
    print(f"CustomerDiscount for CustomerID '{customer_id}' and DiscountCodeID '{discount_code_id}' added to the database.")

# Function to add a customer
def add_customer(name, username, password, gender=None, birthdate=None, phone_number=None, address=None, postal_code=None, created_at=None):
    new_customer = Customer(
        Name=name,
        Gender=gender,
        Birthdate=birthdate,
        PhoneNumber=phone_number,
        Address=address,
        PostalCode=postal_code,
        Username=username,
        Password=hash_password(password),
        CreatedAt=created_at
    )
    session.add(new_customer)
    session.commit()
    print(f"Customer '{name or username}' added to the database.")


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
    return customer.PostalCode

def set_IsNext10Discount(customerID, value):
    customer = session.query(Customer).filter(Customer.CustomerID == customerID).first()
    customer.IsNext10Discount = value
    session.commit()
    print(f"IsNext10Discount for CustomerID '{customerID}' updated to '{customer.IsNext10Discount}'.")

def get_gender(customerID):
    customer = session.query(Customer).filter(Customer.CustomerID == customerID).first()
    return customer.Gender

def get_age(customerID):
    # Query the customer from the database
    customer = session.query(Customer).filter(Customer.CustomerID == customerID).first()
    
    # Check if the customer's birthdate exists
    if customer.Birthdate is None:
        return -1  # Return -1 or handle the missing birthdate appropriately
    
    # Calculate age
    today = datetime.now().date()
    birthdate = customer.Birthdate
    
    # Calculate the difference in years
    age = today.year - birthdate.year
    
    # Adjust the age if the birthdate hasn't occurred yet this year
    if (today.month, today.day) < (birthdate.month, birthdate.day):
        age -= 1
    
    return age