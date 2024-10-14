# models.py
from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean, Text, ForeignKey, TIMESTAMP
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.types import DateTime, DECIMAL as Decimal

Base = declarative_base()

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
    created_at = Column(TIMESTAMP)

class Pizza(Base):
    __tablename__ = 'Pizza'
    PizzaID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(255))
    Description = Column(Text)
    Price = Column(Decimal)
    IsVegetarian = Column(Boolean)
    IsVegan = Column(Boolean)

class Ingredient(Base):
    __tablename__ = 'Ingredient'
    IngredientID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(255))
    Cost = Column(Decimal)

class Drink(Base):
    __tablename__ = 'Drink'
    DrinkID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(255))
    Price = Column(Decimal)

class Dessert(Base):
    __tablename__ = 'Dessert'
    DessertID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(255))
    Price = Column(Decimal)

class Order(Base):
    __tablename__ = 'Order'
    OrderID = Column(Integer, primary_key=True, autoincrement=True)
    CustomerID = Column(Integer, ForeignKey('Customer.CustomerID'))
    OrderDate = Column(TIMESTAMP)
    OrderStatus = Column(String(255))
    EstimatedDeliveryTime = Column(TIMESTAMP)
    TotalPrice = Column(Decimal)
    DiscountApplied = Column(Boolean)
    DeliveryPersonID = Column(Integer, ForeignKey('DeliveryPerson.DeliveryPersonID'))

    customer = relationship("Customer")
    delivery_person = relationship("DeliveryPerson")

class OrderItem(Base):
    __tablename__ = 'OrderItem'
    OrderItemID = Column(Integer, primary_key=True, autoincrement=True)
    OrderID = Column(Integer, ForeignKey('Order.OrderID'))
    ItemType = Column(String(255))
    ItemID = Column(Integer)
    Quantity = Column(Integer)
    Price = Column(Decimal)

    order = relationship("Order")

class DiscountCode(Base):
    __tablename__ = 'DiscountCode'
    DiscountCodeID = Column(Integer, primary_key=True, autoincrement=True)
    Code = Column(String(255))
    Description = Column(Text)
    IsRedeemed = Column(Boolean)
    ExpiryDate = Column(Date)

class CustomerDiscount(Base):
    __tablename__ = 'CustomerDiscount'
    CustomerID = Column(Integer, ForeignKey('Customer.CustomerID'), primary_key=True)
    DiscountCodeID = Column(Integer, ForeignKey('DiscountCode.DiscountCodeID'), primary_key=True)

    customer = relationship("Customer")
    discount_code = relationship("DiscountCode")

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
    DeliveryTime = Column(TIMESTAMP)

    order = relationship("Order")
    delivery_person = relationship("DeliveryPerson")

class EarningsReport(Base):
    __tablename__ = 'EarningsReport'
    ReportID = Column(Integer, primary_key=True, autoincrement=True)
    Month = Column(Integer)
    Year = Column(Integer)
    TotalEarnings = Column(Decimal)
    Region = Column(String(255))
    GenderFilter = Column(String(255))
    AgeFilter = Column(String(255))

class PizzaIngredient(Base):
    __tablename__ = 'PizzaIngredient'
    PizzaID = Column(Integer, ForeignKey('Pizza.PizzaID'), primary_key=True)
    IngredientID = Column(Integer, ForeignKey('Ingredient.IngredientID'), primary_key=True)

    pizza = relationship("Pizza")
    ingredient = relationship("Ingredient")
