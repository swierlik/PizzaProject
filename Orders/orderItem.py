from sqlalchemy import Column, Integer, ForeignKey, DECIMAL, String
from sqlalchemy.orm import relationship
from Orders.ItemType import ItemType
from db import Base, session
from products.dessert import Dessert
from products.drink import Drink
from products.pizza import Pizza

class OrderItem(Base):
    __tablename__ = 'order_items'
    
    OrderItemID = Column(Integer, primary_key=True, autoincrement=True)
    OrderID = Column(Integer, ForeignKey('orderr.OrderID'), nullable=False)  # Corrected ForeignKey
    ItemTypeID = Column(String(50), nullable=False)  # Changed from Enum to String
    ItemID = Column(Integer, nullable=False)
    Quantity = Column(Integer, nullable=False)
    Price = Column(DECIMAL(10, 2), nullable=False)
    
    # Relationship to Order
    order = relationship('Order', back_populates='order_items')

def add_order_item(order_id, item_type_id, item_id, quantity):
    # Fetch the price based on the item type and item ID
    if item_type_id == ItemType.PIZZA:
        item = session.query(Pizza).get(item_id)
        price = item.Price
    elif item_type_id == ItemType.DRINK:
        item = session.query(Drink).get(item_id)
        price = item.Price
    elif item_type_id == ItemType.DESSERT:
        item = session.query(Dessert).get(item_id)
        price = item.Price
    else:
        raise ValueError("Invalid item type.")
    
    price*=quantity
    
    new_order_item = OrderItem(
        OrderID=order_id,
        ItemTypeID=item_type_id,
        ItemID=item_id,
        Quantity=quantity,
        Price=price
    )
    session.add(new_order_item)
    session.commit()
    print(f"Order item with ID {new_order_item.OrderItemID} added successfully.")
    return new_order_item.OrderItemID
