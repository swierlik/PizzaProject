# Orders/Order.py

from sqlalchemy import Column, Integer, String, Boolean, DECIMAL, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from db import Base

class Order(Base):
    __tablename__ = 'orders'  # Renamed from 'Order' to 'orders' to avoid SQL reserved keyword

    OrderID = Column(Integer, primary_key=True, autoincrement=True)
    CustomerID = Column(Integer, ForeignKey('customers.CustomerID'), nullable=False)
    OrderDate = Column(DateTime, nullable=False, server_default=func.now())
    OrderStatus = Column(String(255), nullable=False, default='Pending')
    EstimatedDeliveryTime = Column(DateTime, nullable=True)
    TotalPrice = Column(DECIMAL(10, 2), nullable=False)
    DiscountApplied = Column(Boolean, default=False)
    DeliveryPersonID = Column(Integer, ForeignKey('delivery_persons.DeliveryPersonID'), nullable=True)

    # Relationships
    customer = relationship('Customer', back_populates='orders')
    delivery_person = relationship('DeliveryPerson', back_populates='assigned_orders')
    order_items = relationship('OrderItem', back_populates='order', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Order(OrderID={self.OrderID}, CustomerID={self.CustomerID})>"