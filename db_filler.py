# db_filler.py
import random
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
from models import *
from db_setup import setup_database

def add_entries(session):
    # Insert DeliveryPerson records first
    delivery_person_entries = [DeliveryPerson(
        Name=f'DeliveryPerson {i}',
        AssignedPostalCode=f'PostalCode {i}',
        IsAvailable=random.choice([True, False])
    ) for i in range(5)]
    
    session.add_all(delivery_person_entries)
    session.commit()

    # Insert remaining entries
    for cls in [Customer, Pizza, Ingredient, Drink, Dessert, Order, OrderItem, DiscountCode, CustomerDiscount, Delivery, EarningsReport, PizzaIngredient]:
        entries = []
        for i in range(5):
            if cls == Customer:
                entry = Customer(
                    Name=f'Customer {i}',
                    Gender=random.choice(['Male', 'Female']),
                    Birthdate=datetime(1980, 1, 1) + timedelta(days=random.randint(0, 15000)),
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
                    DeliveryPersonID=random.randint(1, 5)  # Ensure this ID exists in DeliveryPerson
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
                    ExpiryDate=datetime(2024, 1, 1) + timedelta(days=random.randint(0, 365))
                )
            elif cls == CustomerDiscount:
                entry = CustomerDiscount(
                    CustomerID=random.randint(1, 5),
                    DiscountCodeID=random.randint(1, 5)
                )
            elif cls == Delivery:
                entry = Delivery(
                    OrderID=random.randint(1, 5),
                    DeliveryPersonID=random.randint(1, 5),
                    DeliveryStatus=random.choice(['Pending', 'Delivered', 'Failed']),
                    DeliveryTime=datetime.now() + timedelta(minutes=random.randint(1, 60))
                )
            elif cls == EarningsReport:
                entry = EarningsReport(
                    Month=random.randint(1, 12),
                    Year=datetime.now().year,
                    TotalEarnings=Decimal(random.uniform(1000, 5000)),
                    Region=f'Region {i}',
                    GenderFilter=random.choice(['Male', 'Female']),
                    AgeFilter=random.choice(['20-30', '30-40', '40-50', '50+'])
                )
            elif cls == PizzaIngredient:
                entry = PizzaIngredient(
                    PizzaID=random.randint(1, 5),
                    IngredientID=random.randint(1, 5)
                )
            
            entries.append(entry)
        
        session.add_all(entries)
        session.commit()

def main():
    engine = setup_database()
    Session = sessionmaker(bind=engine)
    session = Session()
    
    add_entries(session)
    print("Database has been filled with sample data.")

if __name__ == "__main__":
    main()
