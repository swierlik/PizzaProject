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


# Make na order given the customer ID, order date, and a dictionary of items followed by quantities
def place_order(customer_id, order_date, pizzas, drinks, desserts, discountCode=None):
    order_total = 0
    discount_applied = False
    
    try:
        with SessionLocal() as session:
            # Calculate estimated delivery time
            estimated_delivery_time = order_date + timedelta(minutes=count_orders_live() * 10 + 30)

            # Calculate the total price based on the items before creating the order
            for pizzaID in pizzas.keys():
                add_PizzasOrderedCount(customer_id, 1)
                if get_PizzasOrderedCount(customer_id) % 10 == 0:
                    order_total += get_price_pizza(pizzaID) * 0.9  # Apply discount if applicable
                else:
                    order_total += get_price_pizza(pizzaID)

            for drinkID in drinks.keys():
                order_total += get_price_drink(drinkID)

            for dessertID in desserts.keys():
                order_total += get_price_dessert(dessertID)

            # Apply discount if a discount code is provided
            if discountCode:
                order_total = get_discount_by_code(discountCode, order_total)
                discount_applied = True
            
            # Find available delivery person
            delivery_person_id = find_available_delivery_person(get_postal_code(customer_id))
            if delivery_person_id is None:
                print("No available delivery person found.")
                return
            
            # Create new order
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
            session.commit()  # Commit the order to the database

            # Add order items
            for pizzaID in pizzas.keys():
                session.add(create_order_item(new_order.OrderID, 'PIZZA', pizzaID, pizzas[pizzaID]))
            for drinkID in drinks.keys():
                session.add(create_order_item(new_order.OrderID, 'DRINK', drinkID, drinks[drinkID]))
            for dessertID in desserts.keys():
                session.add(create_order_item(new_order.OrderID, 'DESSERT', dessertID, desserts[dessertID]))

            # Commit all changes if all went well
            session.commit()
            print(f"Order with ID {new_order.OrderID} added successfully.")
    
    except SQLAlchemyError as e:
        print(f"An error occurred: {e}")
        session.rollback()  # Roll back the transaction in case of an error