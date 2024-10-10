from datetime import timedelta
from decimal import Decimal

from sqlalchemy import asc, desc
from Deliveries.DeliveryManagement import find_available_delivery_person, set_availability
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
    return int(session.query(Order).filter(Order.OrderStatus == "Preparing").count())

def get_grouping(postal_code, order_time, my_pizza_count):
    orders = session.query(Order).filter(Order.OrderStatus == "Pending", Order.IsGrouped == False).all()
    good_orders=[]
    pizzas_limit=3
    total_pizzas=my_pizza_count
    if total_pizzas>=pizzas_limit:
        return good_orders
    
    for order in orders:
        if get_postal_code(order.CustomerID) == postal_code and count_pizzas(order.OrderID)+total_pizzas <= pizzas_limit and abs(order.OrderDate - order_time)<=timedelta(minutes=3):
            total_pizzas+=count_pizzas(order.OrderID)
            good_orders.append(order.OrderID)
    return good_orders

#counts total amount of pizzas with said orderID
def count_pizzas(order_id):
    orderItems=session.query(OrderItem).filter(OrderItem.OrderID == order_id, OrderItem.ItemTypeID == ItemType.PIZZA).all()
    total_pizzas=0
    for orderItem in orderItems:
        total_pizzas+=orderItem.Quantity
    return total_pizzas

# counts all pizzes in Preparing 
def count_all_pizzas():
    all_pizzas=0
    with SessionLocal() as session:
        orders = session.query(Order).filter(Order.OrderStatus=="Preparing").all()
        for order in orders:
            all_pizzas+=count_pizzas(order.OrderID)
    return all_pizzas

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

def set_estimated_delivery_time(order_id, estimated_delivery_time):
    with SessionLocal() as session:
        order = session.query(Order).get(order_id)
        order.EstimatedDeliveryTime = estimated_delivery_time
        session.commit()
        print(f"Order {order_id} estimated delivery time updated to {estimated_delivery_time}.")

def set_is_grouped(order_id, is_grouped):
    with SessionLocal() as session:
        order = session.query(Order).get(order_id)
        order.IsGrouped = is_grouped
        session.commit()
        print(f"Order {order_id} is_grouped updated to {is_grouped}.")

# Make an order given the customer ID, order date, and a dictionary of items followed by quantities
def place_order(customer_id, order_date, pizzas, drinks, desserts, discountCode=None, is_grouped=False, estimated_delivery_time=None):
    order_total_before_discount = 0
    discount_applied = False
    discount_total = 0

    try:
        with SessionLocal() as session:
            # Calculate estimated delivery time
            
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

            
            #Calculate Delivery time
            if estimated_delivery_time == None:
                driver = find_available_delivery_person(get_postal_code(customer_id))
                if driver:
                    estimated_delivery_time = order_date + timedelta(minutes=15 + total_pizzas*2 + count_all_pizzas()*2 + 5)
                else:
                    estimated_delivery_time = order_date + timedelta(minutes=30 + total_pizzas*2 + count_all_pizzas()*2 + 5)

            #Assign current estimated delivery time to all grouped orders
            group_orders = get_grouping(get_postal_code(customer_id), order_date, total_pizzas)
            if group_orders:
                is_grouped = True
                for orderID in group_orders:
                    set_estimated_delivery_time(orderID, estimated_delivery_time)
                    set_is_grouped(orderID, is_grouped)


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
                set_IsNext10Discount(customer_id, False)
                discount_total+=discount_amount

            #If customer's birthday then 1 free pizza and drink
            if get_customer_by_id(customer_id).Birthdate == order_date.date():
                pizzas[0] = 1
                drinks[0] = 1

            # Create new order
            new_order = Order(
                CustomerID=customer_id,
                OrderDate=order_date,
                OrderStatus="Pending",
                EstimatedDeliveryTime=estimated_delivery_time,
                TotalPrice=order_total,
                DiscountApplied=discount_applied,
                DeliveryPersonID=None,
                IsGrouped=is_grouped
            )
            #Add 10 pizzas discount to next order
            if passed10:
                set_IsNext10Discount(customer_id, True)

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
        orders = session.query(Order).order_by(asc(Order.EstimatedDeliveryTime)).all()
        for order in orders:
            if order.OrderStatus == "Pending" and (order.OrderDate + timedelta(minutes=5)) < datetime.now():
                order.OrderStatus = "Preparing"
                session.commit()
            if order.OrderStatus == "Preparing" and (order.OrderDate + timedelta(minutes=count_pizzas(order.OrderID)*2 + 5)) < datetime.now():
                order.OrderStatus = "ReadyForDelivery"
                session.commit()
            if order.OrderStatus == "ReadyForDelivery" and find_available_delivery_person(get_postal_code(order.CustomerID))!=None and (order.EstimatedDeliveryTime - timedelta(minutes=15)) < datetime.now():
                assign_driver(order.EstimatedDeliveryTime)
                session.commit()
            if order.OrderStatus == "Delivering" and order.EstimatedDeliveryTime < datetime.now():
                complete_order(order.OrderID)
            if order.OrderStatus== "Completed" and (order.EstimatedDeliveryTime + timedelta(minutes=15)) < datetime.now():
                order.delivery_person.IsAvailable = True
                session.commit()
        session.commit()
        print("Orders refreshed.")


def assign_driver(estimated_delivery_time):
    with SessionLocal() as session:
        orders = session.query(Order).filter(Order.EstimatedDeliveryTime == estimated_delivery_time).all()

        driver = find_available_delivery_person(get_postal_code(orders[0].CustomerID))
        set_availability(driver, False)
        if driver:
            for order in orders:
                order.DeliveryPersonID = driver
                order.OrderStatus = "Delivering"
                order.delivery_person.IsAvailable = False
                session.commit()
                print(f"Order {order.OrderID} assigned to driver {driver}.")
        else:
            print(f"No available driver found for order {orders}.")


def complete_order(order_id):
    with SessionLocal() as session:
        order = session.query(Order).filter(Order.OrderID == order_id).first()
        if order:
            order.OrderStatus = "Completed"
            session.commit()
            print(f"Order {order.OrderID} completed.")
        else:
            print(f"Order {order_id} not found.")


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

            # Convert TotalPrice from Decimal to float
            for order in orders:
                order.TotalPrice = float(order.TotalPrice)  # Convert Decimal to float
            return orders
    except SQLAlchemyError as e:
        print(f"Error fetching orders for customer {customer_id}: {e}")
        return []
