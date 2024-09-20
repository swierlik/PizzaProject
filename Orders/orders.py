# orders/order.py
from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from db import Base, session
from datetime import datetime
from products.dessert import Dessert  # Adjust the import path as necessary

# Define the Order class
class Order(Base):
    __tablename__ = 'Order'
    
    OrderID = Column(Integer, primary_key=True, autoincrement=True)
    CustomerName = Column(String(255), nullable=False)
    OrderDate = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to OrderItem
    order_items = relationship('OrderItem', back_populates='order')


# Function to add an order
def add_order(customer_name, item_id, quantity):
    # Fetch the dessert item from the database
    dessert_item = session.query(Dessert).filter(Dessert.DessertID == item_id).one_or_none()
    if dessert_item is None:
        print(f"Dessert with ID {item_id} does not exist.")
        return
    
    # Calculate total price
    total_price = dessert_item.Price * quantity
    
    new_order = Order(
        CustomerName=customer_name,
        ItemID=item_id,
        Quantity=quantity,
        TotalPrice=total_price
    )
    session.add(new_order)
    session.commit()
    print(f"Order for '{dessert_item.Name}' x {quantity} placed by {customer_name}. Total Price: ${total_price:.2f}")
