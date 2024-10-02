from datetime import timedelta
from Deliveries.DeliveryManagement import find_available_delivery_person
from Orders import ItemType
from Products.ExtrasManagement import get_price_dessert, get_price_drink
from Products.PizzaManagement import get_price_pizza
from db import SessionLocal, session
from Customers.CustomersManagement import *
from models.Drink import Drink
from models.Dessert import Dessert
from models.Order import Order
from models.OrderItem import OrderItem
from models.Pizza import Pizza
from sqlalchemy.exc import SQLAlchemyError


def count_orders_live():
    return int(session.query(Order).filter(Order.OrderStatus != "Completed").count())

def create_order_item(order_id, item_type_id, item_id, quantity):
    # Fetch the price based on the item type and item ID
    if item_type_id == ItemType.PIZZA:
        item = session.query(Pizza).get(item_id)
        price = item.Price
    elif item_type_id == ItemType.DRINK:
        item = session.query(Drink).get(item_id)
        price = item.Price
    elif item_type_id == ItemType.DESSERT:
        item = session.query(Dessert).get(item_id)
        price = item.Price
    else:
        raise ValueError("Invalid item type.")
    
    price*=quantity
    
    new_order_item = OrderItem(
        OrderID=order_id,
        ItemTypeID=item_type_id,
        ItemID=item_id,
        Quantity=quantity,
        Price=price
    )

    return new_order_item


# Make an order given the customer ID, order date, and a dictionary of items followed by quantities
def place_order(customer_id, order_date, pizzas, drinks, desserts, discountCode=None):
    order_total_before_discount = 0
    discount_applied = False
    discount_amount = 0

    try:
        with SessionLocal() as session:
            # Calculate estimated delivery time
            estimated_delivery_time = order_date + timedelta(minutes=count_orders_live() * 10 + 30)

            # Calculate the total price before any discounts
            for pizzaID in pizzas.keys():
                add_PizzasOrderedCount(customer_id, 1)
                if get_PizzasOrderedCount(customer_id) % 10 == 0:
                    order_total_before_discount += get_price_pizza(pizzaID) * 0.9  # Apply 10% discount
                else:
                    order_total_before_discount += get_price_pizza(pizzaID)

            for drinkID in drinks.keys():
                order_total_before_discount += get_price_drink(drinkID)

            for dessertID in desserts.keys():
                order_total_before_discount += get_price_dessert(dessertID)

            # Apply discount if a discount code is provided
            if discountCode:
                discount_amount = get_discount_by_code(discountCode, order_total_before_discount)
                order_total = order_total_before_discount - discount_amount
                discount_applied = True
            else:
                order_total = order_total_before_discount

            # Create new order
            new_order = Order(
                CustomerID=customer_id,
                OrderDate=order_date,
                OrderStatus="Pending",
                EstimatedDeliveryTime=estimated_delivery_time,
                TotalPrice=order_total,
                DiscountApplied=discount_applied,
                DeliveryPersonID=None
            )
            session.add(new_order)
            session.commit()  # Commit the order to the database

            # Add order items
            for pizzaID in pizzas.keys():
                session.add(create_order_item(new_order.OrderID, 'PIZZA', pizzaID, pizzas[pizzaID]))
            for drinkID in drinks.keys():
                session.add(create_order_item(new_order.OrderID, 'DRINK', drinkID, drinks[drinkID]))
            for dessertID in desserts.keys():
                session.add(create_order_item(new_order.OrderID, 'DESSERT', dessertID, desserts[dessertID]))

            session.commit()  # Commit the items

            print(f"Order with ID {new_order.OrderID} added successfully.")

            return new_order, order_total_before_discount, discount_amount

    except SQLAlchemyError as e:
        print(f"An error occurred: {e}")
        session.rollback()  # Roll back the transaction in case of an error



def get_order(order_id):
    with SessionLocal() as session:
        order = session.query(Order).get(order_id)
        return order

def refresh_orders():
    with SessionLocal() as session:
        orders = session.query(Order).all()
        for order in orders:
            if order.OrderStatus == "Delivering" and order.EstimatedDeliveryTime < datetime.now():
                order.OrderStatus = "Completed"
                order.delivery_person.IsAvailable = True
                session.commit()
        session.commit()
        print("Orders refreshed.")


def assign_drivers():
    with SessionLocal() as session:
        orders = session.query(Order).filter(Order.OrderStatus == "Pending").all()
        for order in orders:
            driver = find_available_delivery_person(get_postal_code(order.CustomerID))
            if driver:
                order.DeliveryPersonID = driver
                order.OrderStatus = "Delivering"
                order.delivery_person.IsAvailable = False
                session.commit()
                print(f"Order {order.OrderID} assigned to driver {driver}.")
            else:
                print(f"No available driver found for order {order.OrderID}.")

def assign_driver(order_id):
    with SessionLocal() as session:
        order = session.query(Order).filter(Order.OrderID == order_id).first()
        driver = find_available_delivery_person(get_postal_code(order.CustomerID))
        if driver:
            order.DeliveryPersonID = driver
            order.OrderStatus = "Delivering"
            order.delivery_person.IsAvailable = False
            session.commit()
            print(f"Order {order.OrderID} assigned to driver {driver}.")
        else:
            print(f"No available driver found for order {order.OrderID}.")