from sqlalchemy import Column, Integer, String, Boolean, DECIMAL, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from db import Base, session

# Define the Order class
class Order(Base):
    __tablename__ = 'Orderr'  # Using 'Orderr' to match the table name
    
    OrderID = Column(Integer, primary_key=True, autoincrement=True)
    CustomerID = Column(Integer, ForeignKey('Customer.CustomerID'), nullable=False)
    OrderDate = Column(TIMESTAMP, nullable=False)
    OrderStatus = Column(String(255), nullable=False)
    EstimatedDeliveryTime = Column(TIMESTAMP, nullable=True)
    TotalPrice = Column(DECIMAL(10, 2), nullable=False)
    DiscountApplied = Column(Boolean, default=False)
    DeliveryPersonID = Column(Integer, ForeignKey('DeliveryPerson.DeliveryPersonID'), nullable=True)
    
    # Relationships
    customer = relationship('Customer', backref='orders')  # Link to the Customer table
    delivery_person = relationship('DeliveryPerson', backref='orders')  # Link to the DeliveryPerson table
    order_items = relationship('OrderItem', backref='order', cascade="all, delete-orphan")  # Link to OrderItem table

    def __repr__(self):
        return (f"<Order(OrderID={self.OrderID}, CustomerID={self.CustomerID}, "
                f"OrderDate={self.OrderDate}, OrderStatus='{self.OrderStatus}', "
                f"TotalPrice={self.TotalPrice}, DiscountApplied={self.DiscountApplied})>")

# Example function to add an order
def add_order(customer_id, order_date, order_status, estimated_delivery_time, total_price, discount_applied, delivery_person_id=None):
    new_order = Order(
        CustomerID=customer_id,
        OrderDate=order_date,
        OrderStatus=order_status,
        EstimatedDeliveryTime=estimated_delivery_time,
        TotalPrice=total_price,
        DiscountApplied=discount_applied,
        DeliveryPersonID=delivery_person_id
    )
    session.add(new_order)
    session.commit()
    print(f"Order with ID {new_order.OrderID} added successfully.")
