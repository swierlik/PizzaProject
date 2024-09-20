from sqlalchemy import Column, Integer, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from db import Base, session

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

    def __repr__(self):
        return (f"<OrderItem(OrderItemID={self.OrderItemID}, OrderID={self.OrderID}, "
                f"ItemTypeID={self.ItemTypeID}, ItemID={self.ItemID}, "
                f"Quantity={self.Quantity}, Price={self.Price})>")

# Function to add an order item
def add_order_item(order_id, item_type_id, item_id, quantity, price):
    new_order_item = OrderItem(
        OrderID=order_id,
        ItemTypeID=item_type_id,
        ItemID=item_id,
        Quantity=quantity,
        Price=price
    )
    session.add(new_order_item)
    session.commit()
    print(f"OrderItem for OrderID '{order_id}' added to the database.")

