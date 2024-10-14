from datetime import timedelta, datetime
from decimal import Decimal
import pandas as pd
from sqlalchemy import asc
from Deliveries.DeliveryManagement import find_available_delivery_person
from db import SessionLocal, session
from Customers.CustomersManagement import *
from models.Order import Order
from models.OrderItem import OrderItem
from models.Item import Item
from sqlalchemy.exc import SQLAlchemyError
from enum import Enum

# Define ItemType Enum if not already defined
class ItemType(Enum):
    PIZZA = 'PIZZA'
    DRINK = 'DRINK'
    DESSERT = 'DESSERT'

def get_price_item(item_id):
    item = session.query(Item).get(item_id)
    if item:
        return float(item.Price)
    else:
        raise ValueError("Item not found.")

def count_orders_live():
    return int(session.query(Order).filter(Order.OrderStatus == "Preparing").count())

def get_grouping(postal_code, order_time, my_pizza_count):
    orders = session.query(Order).filter(Order.OrderStatus == "Pending", Order.IsGrouped == False).all()
    good_orders = []
    pizzas_limit = 3
    total_pizzas = my_pizza_count
    if total_pizzas >= pizzas_limit:
        return good_orders
    
    for order in orders:
        if (get_postal_code(order.CustomerID) == postal_code and
            count_pizzas(order.OrderID) + total_pizzas <= pizzas_limit and
            abs(order.OrderDate - order_time) <= timedelta(minutes=3)):
            total_pizzas += count_pizzas(order.OrderID)
            good_orders.append(order.OrderID)
    return good_orders

def count_pizzas(order_id):
    order_items = session.query(OrderItem).filter(
        OrderItem.OrderID == order_id,
        OrderItem.ItemTypeID == ItemType.PIZZA.value
    ).all()
    total_pizzas = sum(order_item.Quantity for order_item in order_items)
    return total_pizzas

def count_all_pizzas():
    all_pizzas = 0
    with SessionLocal() as session:
        orders = session.query(Order).filter(Order.OrderStatus == "Preparing").all()
        for order in orders:
            all_pizzas += count_pizzas(order.OrderID)
    return all_pizzas

def create_order_item(order_id, item_type_id, item_id, quantity):
    item = session.query(Item).get(item_id)
    if item is None:
        raise ValueError("Item not found.")
    if item.ItemType != item_type_id:
        raise ValueError("ItemType mismatch.")
    price = item.Price * quantity
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

def place_order(customer_id, order_date, pizzas, drinks, desserts, discountCode=None, is_grouped=False, estimated_delivery_time=None):
    order_total_before_discount = 0
    discount_applied = False
    discount_total = 0

    try:
        with SessionLocal() as session:
            passed10 = False
            total_pizzas = 0
            if pizzas:
                for pizzaID in pizzas.keys():
                    for _ in range(pizzas[pizzaID]):
                        total_pizzas += 1
                        add_PizzasOrderedCount(customer_id, 1)
                        if get_PizzasOrderedCount(customer_id) % 10 == 0:
                            passed10 = True
                    order_total_before_discount += get_price_item(pizzaID) * pizzas[pizzaID]
            else:
                raise ValueError("No pizzas in the order.")

            for drinkID in drinks.keys():
                order_total_before_discount += get_price_item(drinkID) * drinks[drinkID]

            for dessertID in desserts.keys():
                order_total_before_discount += get_price_item(dessertID) * desserts[dessertID]

            if estimated_delivery_time is None:
                driver = find_available_delivery_person(get_postal_code(customer_id))
                time_offset = 15 if driver else 30
                estimated_delivery_time = order_date + timedelta(
                    minutes=time_offset + total_pizzas * 2 + count_all_pizzas() * 2 + 5
                )

            group_orders = get_grouping(get_postal_code(customer_id), order_date, total_pizzas)
            if group_orders:
                is_grouped = True
                for orderID in group_orders:
                    set_estimated_delivery_time(orderID, estimated_delivery_time)
                    set_is_grouped(orderID, is_grouped)

            if discountCode:
                discount_amount = get_discount_by_code(discountCode, order_total_before_discount)
                order_total = order_total_before_discount - discount_amount
                print(f"\n\nDiscount applied by code: {discountCode}!\n\n")
                discount_applied = True
                discount_total += discount_amount
            else:
                order_total = order_total_before_discount

            if get_customer_by_id(customer_id).IsNext10Discount:
                discount_amount = order_total * 0.1
                order_total -= discount_amount
                discount_applied = True
                print("\n\nDiscount applied by 10th pizza!\n\n")
                set_IsNext10Discount(customer_id, False)
                discount_total += discount_amount

            if get_customer_by_id(customer_id).Birthdate:
                customer_birth = get_customer_by_id(customer_id).Birthdate
                customer_day = customer_birth.day
                customer_month = customer_birth.month
                order_day = order_date.day
                order_month = order_date.month
                if customer_day == order_day and customer_month == order_month:
                    pizzas[11] = 1
                    drinks[1] = 1

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
            if passed10:
                set_IsNext10Discount(customer_id, True)

            session.add(new_order)
            session.commit()

            for pizzaID in pizzas.keys():
                session.add(create_order_item(new_order.OrderID, 'PIZZA', pizzaID, pizzas[pizzaID]))
            for drinkID in drinks.keys():
                session.add(create_order_item(new_order.OrderID, 'DRINK', drinkID, drinks[drinkID]))
            for dessertID in desserts.keys():
                session.add(create_order_item(new_order.OrderID, 'DESSERT', dessertID, desserts[dessertID]))

            session.commit()
            print(f"Order with ID {new_order.OrderID} added successfully.")

            return new_order, order_total_before_discount, discount_total

    except SQLAlchemyError as e:
        print(f"An error occurred: {e}")
        session.rollback()

def get_order(order_id):
    with SessionLocal() as session:
        order = session.query(Order).get(order_id)
        return order

def get_order_items(order_id):
    with SessionLocal() as session:
        order_items = session.query(OrderItem).filter(OrderItem.OrderID == order_id).all()
        return order_items

def order_items_to_list(order_items, session):
    items = []
    for order_item in order_items:
        item = session.query(Item).get(order_item.ItemID)
        item_name = item.Name if item else "Unknown item"
        items.append({
            "item_name": item_name,
            "quantity": order_item.Quantity,
            "price": float(order_item.Price)
        })
    return items

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
            if (order.OrderStatus == "ReadyForDelivery" and
                find_available_delivery_person(get_postal_code(order.CustomerID)) is not None and
                (order.EstimatedDeliveryTime - timedelta(minutes=15)) < datetime.now()):
                assign_driver(order.EstimatedDeliveryTime, get_postal_code(order.CustomerID))
                session.commit()
            if order.OrderStatus == "Delivering" and order.EstimatedDeliveryTime < datetime.now():
                complete_order(order.OrderID)
            if order.OrderStatus == "Completed" and (order.EstimatedDeliveryTime + timedelta(minutes=15)) < datetime.now():
                order.delivery_person.IsAvailable = True
                session.commit()
        session.commit()
        print("Orders refreshed.")

def assign_driver(estimated_delivery_time, postal_code):
    with SessionLocal() as session:
        orders = session.query(Order).filter(Order.EstimatedDeliveryTime == estimated_delivery_time).all()
        print(f"Assigning driver to orders {orders}.\n\n")
        driver = find_available_delivery_person(postal_code)

        if driver:
            for order in orders:
                order.DeliveryPersonID = driver
                order.OrderStatus = "Delivering"
                order.delivery_person.IsAvailable = False
                session.commit()
                print(f"Order {order.OrderID} assigned to driver {driver}.")
        else:
            print(f"No available driver found for orders {orders}.")

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
    try:
        with SessionLocal() as session:
            order = session.query(Order).filter_by(OrderID=order_id).first()
            if not order:
                return False
            time_since_order = datetime.now() - order.OrderDate
            return (time_since_order <= timedelta(minutes=5)) and (order.OrderStatus not in ["Canceled", "Completed"])
    except SQLAlchemyError as e:
        print(f"Error checking if order can be canceled: {e}")
        return False

def get_order_by_customer(customer_id):
    try:
        with SessionLocal() as session:
            orders = session.query(Order).filter_by(CustomerID=customer_id).order_by(Order.OrderDate.desc()).all()
            for order in orders:
                order.TotalPrice = float(order.TotalPrice)
            return orders
    except SQLAlchemyError as e:
        print(f"Error fetching orders for customer {customer_id}: {e}")
        return []

def get_financial_summary(month=None, postal_code=None, gender=None, age_group=None):
    if age_group:
        age_group = age_group.split("-")

    try:
        with SessionLocal() as session:
            orders = session.query(Order).all()
            if month:
                orders = [order for order in orders if order.OrderDate.strftime("%B") == month]
            if postal_code:
                orders = [order for order in orders if get_postal_code(order.CustomerID) == postal_code]
            if gender:
                orders = [order for order in orders if get_gender(order.CustomerID) == gender]
            if age_group:
                orders = [order for order in orders if float(age_group[0]) <= get_age(order.CustomerID) <= float(age_group[1])]

        orders = pd.DataFrame([order.__dict__ for order in orders])
        if "_sa_instance_state" in orders.columns:
            orders.drop(columns=["_sa_instance_state"], inplace=True)
        orders["TotalPrice"] = orders["TotalPrice"].astype(float)
        return orders
    except SQLAlchemyError as e:
        print(f"Error fetching financial summary: {e}")
        return []
    
def get_orders_by_status(status):
    with SessionLocal() as session:
        orders = session.query(Order).filter_by(OrderStatus=status).all()
        return orders
    
def orders_to_pizzas():
    orders = get_orders_by_status("Preparing")
    pizzas = {}
    for order in orders:
        order_items = get_order_items(order.OrderID)
        for order_item in order_items:
            if order_item.ItemTypeID == ItemType.PIZZA.value:
                item = session.query(Item).get(order_item.ItemID)
                if item.Name in pizzas:
                    pizzas[item.Name] += order_item.Quantity
                else:
                    pizzas[item.Name] = order_item.Quantity
    df = pd.DataFrame(pizzas.items(), columns=["Pizza", "Quantity"])
    return df
