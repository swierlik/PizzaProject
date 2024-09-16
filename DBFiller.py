from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean, ForeignKey, DateTime
from sqlalchemy.types import DECIMAL, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import random
from datetime import datetime, timedelta
from decimal import Decimal

Base = declarative_base()

# Define your models
class Customer(Base):
    __tablename__ = 'Customer'
    CustomerID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(255))
    Gender = Column(String(255))
    Birthdate = Column(Date)
    PhoneNumber = Column(String(255))
    Address = Column(String(255))
    Username = Column(String(255))
    Password = Column(String(255))
    PizzasOrderedCount = Column(Integer)
    role = Column(String(255))
    created_at = Column(DateTime)

class Pizza(Base):
    __tablename__ = 'Pizza'
    PizzaID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(255))
    Description = Column(Text)
    Price = Column(DECIMAL)
    IsVegetarian = Column(Boolean)
    IsVegan = Column(Boolean)

class Ingredient(Base):
    __tablename__ = 'Ingredient'
    IngredientID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(255))
    Cost = Column(DECIMAL)

class Drink(Base):
    __tablename__ = 'Drink'
    DrinkID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(255))
    Price = Column(DECIMAL)

class Dessert(Base):
    __tablename__ = 'Dessert'
    DessertID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(255))
    Price = Column(DECIMAL)

class Order(Base):
    __tablename__ = 'Order'
    OrderID = Column(Integer, primary_key=True, autoincrement=True)
    CustomerID = Column(Integer, ForeignKey('Customer.CustomerID'))
    OrderDate = Column(DateTime)
    OrderStatus = Column(String(255))
    EstimatedDeliveryTime = Column(DateTime)
    TotalPrice = Column(DECIMAL)
    DiscountApplied = Column(Boolean)
    DeliveryPersonID = Column(Integer, ForeignKey('DeliveryPerson.DeliveryPersonID'))

class OrderItem(Base):
    __tablename__ = 'OrderItem'
    OrderItemID = Column(Integer, primary_key=True, autoincrement=True)
    OrderID = Column(Integer, ForeignKey('Order.OrderID'))
    ItemType = Column(String(255))
    ItemID = Column(Integer)
    Quantity = Column(Integer)
    Price = Column(DECIMAL)

class DiscountCode(Base):
    __tablename__ = 'DiscountCode'
    DiscountCodeID = Column(Integer, primary_key=True, autoincrement=True)
    Code = Column(String(255))
    Description = Column(Text)
    IsRedeemed = Column(Boolean)
    ExpiryDate = Column(Date)

class CustomerDiscount(Base):
    __tablename__ = 'CustomerDiscount'
    CustomerID = Column(Integer, ForeignKey('Customer.CustomerID'))
    DiscountCodeID = Column(Integer, ForeignKey('DiscountCode.DiscountCodeID'))

class DeliveryPerson(Base):
    __tablename__ = 'DeliveryPerson'
    DeliveryPersonID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(255))
    AssignedPostalCode = Column(String(255))
    IsAvailable = Column(Boolean)

class Delivery(Base):
    __tablename__ = 'Delivery'
    DeliveryID = Column(Integer, primary_key=True, autoincrement=True)
    OrderID = Column(Integer, ForeignKey('Order.OrderID'))
    DeliveryPersonID = Column(Integer, ForeignKey('DeliveryPerson.DeliveryPersonID'))
    DeliveryStatus = Column(String(255))
    DeliveryTime = Column(DateTime)

class EarningsReport(Base):
    __tablename__ = 'EarningsReport'
    ReportID = Column(Integer, primary_key=True, autoincrement=True)
    Month = Column(Integer)
    Year = Column(Integer)
    TotalEarnings = Column(DECIMAL)
    Region = Column(String(255))
    GenderFilter = Column(String(255))
    AgeFilter = Column(String(255))

class PizzaIngredient(Base):
    __tablename__ = 'PizzaIngredient'
    PizzaID = Column(Integer, ForeignKey('Pizza.PizzaID'))
    IngredientID = Column(Integer, ForeignKey('Ingredient.IngredientID'))

# Database setup
DATABASE_URL = "mysql+mysqlconnector://username:password@localhost/pizza_project"
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# Create tables
Base.metadata.create_all(engine)

# Helper function to generate random data
def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))

def add_entries():
    for cls in [Customer, Pizza, Ingredient, Drink, Dessert, Order, OrderItem, DiscountCode, CustomerDiscount, DeliveryPerson, Delivery, EarningsReport, PizzaIngredient]:
        entries = []
        for i in range(5):
            if cls == Customer:
                entry = Customer(
                    Name=f'Customer {i}',
                    Gender=random.choice(['Male', 'Female']),
                    Birthdate=random_date(datetime(1980, 1, 1), datetime(2000, 1, 1)),
                    PhoneNumber=f'555-000{i}',
                    Address=f'Address {i}',
                    Username=f'user{i}',
                    Password=f'pass{i}',
                    PizzasOrderedCount=random.randint(0, 10),
                    role=random.choice(['Customer', 'Admin']),
                    created_at=datetime.now()
                )
            elif cls == Pizza:
                entry = Pizza(
                    Name=f'Pizza {i}',
                    Description=f'Description {i}',
                    Price=Decimal(random.uniform(5, 20)),
                    IsVegetarian=random.choice([True, False]),
                    IsVegan=random.choice([True, False])
                )
            elif cls == Ingredient:
                entry = Ingredient(
                    Name=f'Ingredient {i}',
                    Cost=Decimal(random.uniform(1, 10))
                )
            elif cls == Drink:
                entry = Drink(
                    Name=f'Drink {i}',
                    Price=Decimal(random.uniform(1, 5))
                )
            elif cls == Dessert:
                entry = Dessert(
                    Name=f'Dessert {i}',
                    Price=Decimal(random.uniform(2, 8))
                )
            elif cls == Order:
                entry = Order(
                    CustomerID=random.randint(1, 5),
                    OrderDate=datetime.now(),
                    OrderStatus=random.choice(['Pending', 'Completed', 'Cancelled']),
                    EstimatedDeliveryTime=datetime.now() + timedelta(hours=random.randint(1, 2)),
                    TotalPrice=Decimal(random.uniform(10, 50)),
                    DiscountApplied=random.choice([True, False]),
                    DeliveryPersonID=random.randint(1, 5)
                )
            elif cls == OrderItem:
                entry = OrderItem(
                    OrderID=random.randint(1, 5),
                    ItemType=random.choice(['Pizza', 'Drink', 'Dessert']),
                    ItemID=random.randint(1, 5),
                    Quantity=random.randint(1, 3),
                    Price=Decimal(random.uniform(1, 20))
                )
            elif cls == DiscountCode:
                entry = DiscountCode(
                    Code=f'DISCOUNT{i}',
                    Description=f'Description {i}',
                    IsRedeemed=random.choice([True, False]),
                    ExpiryDate=random_date(datetime(2024, 1, 1), datetime(2024, 12, 31))
                )
            elif cls == CustomerDiscount:
                entry = CustomerDiscount(
                    CustomerID=random.randint(1, 5),
                    DiscountCodeID=random.randint(1, 5)
                )
            elif cls == DeliveryPerson:
                entry = DeliveryPerson(
                    Name=f'DeliveryPerson {i}',
                    AssignedPostalCode=f'PostalCode {i}',
                    IsAvailable=random.choice([True, False])
                )
            elif cls == Delivery:
                entry = Delivery(
                    OrderID=random.randint(1, 5),
                    DeliveryPersonID=random.randint(1, 5),
                    DeliveryStatus=random.choice(['Pending', 'Delivered']),
                    DeliveryTime=datetime.now()
                )
            elif cls == EarningsReport:
                entry = EarningsReport(
                    Month=random.randint(1, 12),
                    Year=datetime.now().year,
                    TotalEarnings=Decimal(random.uniform(1000, 5000)),
                    Region=f'Region {i}',
                    GenderFilter=random.choice(['Male', 'Female']),
                    AgeFilter=f'{random.randint(18, 65)}-65'
                )
            elif cls == PizzaIngredient:
                entry = PizzaIngredient(
                    PizzaID=random.randint(1, 5),
                    IngredientID=random.randint(1, 5)
                )
            
            entries.append(entry)

        session.add_all(entries)
        session.commit()
        print(f'Added 5 entries to {cls.__tablename__}')

# Run the function to add entries
if __name__ == '__main__':
    add_entries()
