from datetime import timedelta
from sqlalchemy import Column, Integer, String, Boolean, DECIMAL, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from Orders.orderItem import create_order_item
from products import pizza, drink, dessert
from Customer.discountCode import get_discount_by_code
from Customer.customer import get_PizzasOrderedCount, add_PizzasOrderedCount, get_postal_code
from Delivery.deliveryPerson import find_available_delivery_person
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

def count_orders_live():
    return session.query(Order).filter(Order.OrderStatus != "Completed").count()

# Make na order given the customer ID, order date, and a dictionary of items followed by quantities
def place_order(customer_id, order_date, pizzas, drinks, desserts, discountCode):
    #Calculate estimated delivery time
    estimated_delivery_time = order_date + timedelta(minutes=count_orders_live*10+30)

        
    order_total = 0
    for Pizza in pizzas.keys():
        add_PizzasOrderedCount(customer_id, 1)
        if get_PizzasOrderedCount(customer_id) %10:
            order_total += pizza.get_price(Pizza) * 0.9
        else:
            order_total += pizza.get_price(Pizza)
        session.add(create_order_item(new_order.OrderID, 'PIZZA', Pizza, pizzas[Pizza]))
        
    for Drink in drinks.keys():
        order_total += drink.get_price(Drink)
        session.add(create_order_item(new_order.OrderID, 'DRINK', Drink, drinks[Drink]))
    for Dessert in desserts.keys():
        order_total += dessert.get_price(Dessert)
        session.add(create_order_item(new_order.OrderID, 'DESSERT', Dessert, desserts[Dessert]))

    discount_applied = False
    if discountCode:
        order_total = get_discount_by_code(discountCode, order_total)

    delivery_person_id= find_available_delivery_person(get_postal_code(customer_id))
    if delivery_person_id is None:
        print("No available delivery person found.")
        return
    

    new_order = Order(
        CustomerID=customer_id,
        OrderDate=order_date,
        OrderStatus="Pending",
        EstimatedDeliveryTime=estimated_delivery_time,
        TotalPrice=order_total,
        DiscountApplied=discount_applied,
        DeliveryPersonID=delivery_person_id
    )
    session.add(new_order)
    session.commit()
    print(f"Order with ID {new_order.OrderID} added successfully.")