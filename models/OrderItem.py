# Orders/OrderItem.py

from sqlalchemy import Column, Integer, ForeignKey, DECIMAL, String
from sqlalchemy.orm import relationship
from database import Base

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

