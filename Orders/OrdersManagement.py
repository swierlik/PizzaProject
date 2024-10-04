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
    discount_total = 0

    try:
        with SessionLocal() as session:
            # Calculate estimated delivery time
            estimated_delivery_time = order_date + timedelta(minutes=pizzas * 10 + 30)
            passed10=False
            # Calculate the total price before any discounts
            total_pizzas=0
            if pizzas:
                for pizzaID in pizzas.keys():
                    for i in range(pizzas[pizzaID]):
                        total_pizzas+=1
                        add_PizzasOrderedCount(customer_id, 1)
                        if get_PizzasOrderedCount(customer_id) % 10 == 0:
                            passed10=True
                    order_total_before_discount += get_price_pizza(pizzaID)*pizzas[pizzaID]
            else:
                exception = ValueError("No pizzas in the order.")
                raise exception

            for drinkID in drinks.keys():
                order_total_before_discount += get_price_drink(drinkID)*drinks[drinkID]

            for dessertID in desserts.keys():
                order_total_before_discount += get_price_dessert(dessertID)*desserts[dessertID]

            # Apply discount if a discount code is provided
            if discountCode:
                discount_amount = get_discount_by_code(discountCode, order_total_before_discount)
                order_total = order_total_before_discount - discount_amount
                discount_applied = True
                discount_total+=discount_amount
            else:
                order_total = order_total_before_discount
            
            #Apply discount if customer has ordered 10 pizzas
            if get_customer_by_id(customer_id).IsNext10Discount:
                discount_amount = order_total*0.1
                order_total = order_total - discount_amount
                discount_applied = True
                get_customer_by_id(customer_id).IsNext10Discount = False
                discount_total+=discount_amount

            #If customer's birthday then 1 free pizza and drink
            if get_customer_by_id(customer_id).Birthdate == order_date.date():
                pizzas[0] = 1
                drinks[0] = 1

            # Create new order
            new_order = Order(
                CustomerID=customer_id,
                OrderDate=order_date,
                OrderStatus="Preparing",
                EstimatedDeliveryTime=estimated_delivery_time,
                TotalPrice=order_total,
                DiscountApplied=discount_applied,
                DeliveryPersonID=None
            )
            #Add 10 pizzas discount to next order
            if passed10:
                get_customer_by_id(customer_id).IsNext10Discount = True

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

            return new_order, order_total_before_discount, discount_total

    except SQLAlchemyError as e:
        print(f"An error occurred: {e}")
        session.rollback()  # Roll back the transaction in case of an error

def get_order(order_id):
    with SessionLocal() as session:
        order = session.query(Order).get(order_id)
        return order

def refresh_orders_status():
    with SessionLocal() as session:
        orders = session.query(Order).all()
        for order in orders:
            if order.OrderStatus == "Preparing" and (order.OrderDate + timedelta(minutes=3)) < datetime.now():
                order.OrderStatus = "ReadyForDelivery"
                session.commit()
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


def can_cancel_order(order_id):
    """
    Check if the order can be canceled.
    An order can be canceled if less than 5 minutes have passed since the order was placed
    and the order is not already canceled or completed.
    """
    try:
        with SessionLocal() as session:
            order = session.query(Order).filter_by(OrderID=order_id).first()
            if not order:
                return False  # Order does not exist

            time_since_order = datetime.now() - order.OrderDate
            return (time_since_order <= timedelta(minutes=5)) and (order.OrderStatus not in ["Canceled", "Completed"])
    except SQLAlchemyError as e:
        print(f"Error checking if order can be canceled: {e}")
        return False

def get_order_by_customer(customer_id):
    """
    Retrieve all orders for a given customer, ordered by OrderDate descending.
    """
    try:
        with SessionLocal() as session:
            orders = session.query(Order).filter_by(CustomerID=customer_id).order_by(Order.OrderDate.desc()).all()
            return orders
    except SQLAlchemyError as e:
        print(f"Error fetching orders for customer {customer_id}: {e}")
        return []