# orders/order.py
from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from db import Base, session
from datetime import datetime
from products.dessert import Dessert  # Adjust the import path as necessary

class Order(Base):
    __tablename__ = 'orderr'  # Use plural form for table names for consistency
    
    OrderID = Column(Integer, primary_key=True, autoincrement=True)
    CustomerName = Column(String(255), nullable=False)
    OrderDate = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to OrderItem
    order_items = relationship('OrderItem', back_populates='order', cascade='all, delete-orphan')
