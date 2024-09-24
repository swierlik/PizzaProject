from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from db import Base
from datetime import datetime

class Order(Base):
    __tablename__ = 'orderr'  # Ensure this matches the ForeignKey in OrderItem
    
    OrderID = Column(Integer, primary_key=True, autoincrement=True)
    CustomerName = Column(String(255), nullable=False)
    OrderDate = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to OrderItem
    order_items = relationship('OrderItem', back_populates='order', cascade='all, delete-orphan')
