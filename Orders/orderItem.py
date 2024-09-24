from sqlalchemy import Column, Integer, ForeignKey, DECIMAL, String
from sqlalchemy.orm import relationship
from db import Base

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
