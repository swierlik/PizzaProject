from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from database import engine, Base

# Create a configured "Session" class
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

# Import your models from the respective files
from models.Customer import Customer
from models.DiscountCode import DiscountCode
from models.CustomerDiscount import CustomerDiscount
from models.Order import Order
from models.OrderItem import OrderItem
from models.Item import Item
from models.Ingredient import Ingredient
from models.DeliveryPerson import DeliveryPerson
from models.ItemIngredient import ItemIngredient

# Function to drop all tables (clearing the database)
def drop_all_tables():
    with engine.connect() as connection:
        # Disable foreign key checks
        connection.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))

        # Drop tables in reverse order of dependencies
        Base.metadata.drop_all(bind=engine, tables=[
            CustomerDiscount.__table__,    # Drop CustomerDiscount first
            DiscountCode.__table__,        # Then DiscountCode
            OrderItem.__table__,           # Then OrderItem
            Order.__table__,               # Then Order
            DeliveryPerson.__table__,      # Then DeliveryPerson
            ItemIngredient.__table__,     # Then PizzaIngredient
            Item.__table__,                # Then Item
            Ingredient.__table__,          # Then Ingredient
            Customer.__table__,            # Drop Customer last
        ])

        # Re-enable foreign key checks
        connection.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))

# Function to create all tables
def create_all_tables():
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    print("Dropping all existing tables...")
    drop_all_tables()  # Drops the tables first to clear the DB

    print("Creating all tables...")
    create_all_tables()  # Then creates all tables again

    print("Database has been reset and reinitialized.")
