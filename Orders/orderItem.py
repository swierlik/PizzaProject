# Orders/OrderItem.py

from sqlalchemy import Column, Integer, ForeignKey, DECIMAL, String
from sqlalchemy.orm import relationship
from db import Base, session
from Orders.ItemType import ItemType
from products.pizza import Pizza
from products.drink import Drink
from products.dessert import Dessert

class OrderItem(Base):
    __tablename__ = 'order_items'

    OrderItemID = Column(Integer, primary_key=True, autoincrement=True)
    OrderID = Column(Integer, ForeignKey('orders.OrderID'), nullable=False)
    ItemTypeID = Column(String(50), nullable=False)
    ItemID = Column(Integer, nullable=False)
    Quantity = Column(Integer, nullable=False)
    Price = Column(DECIMAL(10, 2), nullable=False)

    # Relationship to Order using string-based reference
    order = relationship('Order', back_populates='order_items')

    def __repr__(self):
        return (f"<OrderItem(OrderItemID={self.OrderItemID}, OrderID={self.OrderID}, "
                f"ItemTypeID='{self.ItemTypeID}', ItemID={self.ItemID}, "
                f"Quantity={self.Quantity}, Price={self.Price})>")

def add_order_item(order_id, item_type_id, item_id, quantity):
    # Fetch the price based on the item type and item ID
    if item_type_id == ItemType.PIZZA:
        item = session.query(Pizza).get(item_id)
    elif item_type_id == ItemType.DRINK:
        item = session.query(Drink).get(item_id)
    elif item_type_id == ItemType.DESSERT:
        item = session.query(Dessert).get(item_id)
    else:
        raise ValueError("Invalid item type.")

    if not item:
        raise ValueError(f"Item with ID {item_id} not found.")

    price = float(item.Price) * quantity

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

def add_order_item(order_id, item_type_id, item_id, quantity):
    # Fetch the price based on the item type and item ID
    if item_type_id == ItemType.PIZZA:
        item = session.query(Pizza).get(item_id)
    elif item_type_id == ItemType.DRINK:
        item = session.query(Drink).get(item_id)
    elif item_type_id == ItemType.DESSERT:
        item = session.query(Dessert).get(item_id)
    else:
        raise ValueError("Invalid item type.")

    if not item:
        raise ValueError(f"Item with ID {item_id} not found.")

    price = float(item.Price) * quantity

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
