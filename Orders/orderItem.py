# orders/OrderItem.py
from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from db import Base, session
from datetime import datetime
from products.dessert import Dessert  # Adjust the import path as necessary

class OrderItem(Base):
    __tablename__ = 'OrderItem'
    
    OrderItemID = Column(Integer, primary_key=True, autoincrement=True)
    OrderID = Column(Integer, ForeignKey('Order.OrderID'), nullable=False)
    ItemTypeID = Column(Integer, nullable=False)
    ItemID = Column(Integer, nullable=False)
    Quantity = Column(Integer, nullable=False)
    Price = Column(DECIMAL(10, 2), nullable=False)
    
    # Relationships
    order = relationship('Order', back_populates='order_items')
