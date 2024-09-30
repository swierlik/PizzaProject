# db.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLAlchemy base class
Base = declarative_base()

# Database connection URL
DATABASE_URL = 'mysql+pymysql://root:password@localhost/pizza_project'  # Replace with your credentials

# Create engine
engine = create_engine(DATABASE_URL, echo=True)

# Create a configured "Session" class
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

# Import models to register them with SQLAlchemy
from Customer.customer import Customer
from Orders.Order import Order
from Orders.OrderItem import OrderItem
from Delivery.DeliveryPerson import DeliveryPerson
from products.pizza import Pizza
from products.drink import Drink
from products.dessert import Dessert
from products.ingredient import Ingredient

from Customer.discountCode import DiscountCode

# Function to create all tables
def create_all_tables():
    Base.metadata.create_all(engine)
