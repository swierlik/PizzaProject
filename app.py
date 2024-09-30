# app.py

import sys
import os
from flask import Flask, render_template, request
from sqlalchemy.orm import scoped_session
import threading
import webbrowser

# Add project root to sys.path to resolve imports
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import database session and Base
from db import Base, session as db_session, create_all_tables

# Import Models
from Orders import Order, OrderItem, ItemType
from products.pizza import Pizza
from products.drink import Drink
from products.dessert import Dessert

app = Flask(__name__)

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.close()

@app.route('/')
def home():
    try:
        # Retrieve products from the database
        pizzas = db_session.query(Pizza).all()
        drinks = db_session.query(Drink).all()
        desserts = db_session.query(Dessert).all()
    except Exception as e:
        return f"An error occurred while fetching products: {e}", 500

    return render_template('home.html', pizzas=pizzas, drinks=drinks, desserts=desserts)

@app.route('/place_order', methods=['POST'])
def place_order():
    try:
        customer_name = request.form.get('customer_name', 'Guest').strip()
        if not customer_name:
            customer_name = 'Guest'

        # For simplicity, create a guest customer or fetch existing
        from Customer.customer import Customer

        customer = db_session.query(Customer).filter_by(Name=customer_name).first()
        if not customer:
            customer = Customer(Name=customer_name)
            db_session.add(customer)
            db_session.commit()

        # Create a new Order
        new_order = Order(CustomerID=customer.CustomerID, TotalPrice=0.0)
        db_session.add(new_order)
        db_session.commit()  # Commit to get the OrderID

        ordered_items = []
        total_cost = 0.0

        # Process pizzas
        for pizza in db_session.query(Pizza).all():
            quantity_str = request.form.get(f'quantity_pizza_{pizza.PizzaID}', '0')
            quantity = int(quantity_str) if quantity_str.isdigit() else 0

            if quantity > 0:
                order_item = OrderItem(
                    OrderID=new_order.OrderID,
                    ItemTypeID=ItemType.PIZZA,
                    ItemID=pizza.PizzaID,
                    Quantity=quantity,
                    Price=float(pizza.Price) * quantity
                )
                db_session.add(order_item)
                ordered_items.append((pizza, quantity))
                total_cost += float(pizza.Price) * quantity

        # Process drinks
        for drink in db_session.query(Drink).all():
            quantity_str = request.form.get(f'quantity_drink_{drink.DrinkID}', '0')
            quantity = int(quantity_str) if quantity_str.isdigit() else 0

            if quantity > 0:
                order_item = OrderItem(
                    OrderID=new_order.OrderID,
                    ItemTypeID=ItemType.DRINK,
                    ItemID=drink.DrinkID,
                    Quantity=quantity,
                    Price=float(drink.Price) * quantity
                )
                db_session.add(order_item)
                ordered_items.append((drink, quantity))
                total_cost += float(drink.Price) * quantity

        # Process desserts
        for dessert in db_session.query(Dessert).all():
            quantity_str = request.form.get(f'quantity_dessert_{dessert.DessertID}', '0')
            quantity = int(quantity_str) if quantity_str.isdigit() else 0

            if quantity > 0:
                order_item = OrderItem(
                    OrderID=new_order.OrderID,
                    ItemTypeID=ItemType.DESSERT,
                    ItemID=dessert.DessertID,
                    Quantity=quantity,
                    Price=float(dessert.Price) * quantity
                )
                db_session.add(order_item)
                ordered_items.append((dessert, quantity))
                total_cost += float(dessert.Price) * quantity

        if not ordered_items:
            return "You didn't order anything!", 400

        # Update the total price in the order
        new_order.TotalPrice = total_cost
        db_session.commit()

        # Estimated time (for example purposes, we set it to 30 minutes)
        estimated_time = 30

        return render_template('order_confirmation.html', ordered_items=ordered_items, customer_name=customer_name, total_cost=total_cost, estimated_time=estimated_time)
    except Exception as e:
        db_session.rollback()
        return f"An error occurred while placing your order: {e}", 500

if __name__ == '__main__':
    create_all_tables()  # Create tables if they don't exist
    threading.Timer(1, open_browser).start()
    app.run(debug=True)
