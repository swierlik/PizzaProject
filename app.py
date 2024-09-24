from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import threading
import webbrowser

# Import Base from db.py
from db import Base

# Import Models
from Orders.order import Order
from Orders.orderItem import OrderItem
from Orders.ItemType import ItemType

from products.pizza import Pizza
from products.drink import Drink
from products.dessert import Dessert

app = Flask(__name__)

# Database configuration
engine = create_engine('mysql+pymysql://root:password@localhost/pizza_project')  # Update with your database URL
Base.metadata.bind = engine
SessionLocal = sessionmaker(bind=engine)
Session = scoped_session(SessionLocal)

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

@app.teardown_appcontext
def shutdown_session(exception=None):
    Session.remove()

@app.route('/')
def home():
    session = Session()
    try:
        # Retrieve products from the database
        pizzas = session.query(Pizza).all()
        drinks = session.query(Drink).all()
        desserts = session.query(Dessert).all()
    except Exception as e:
        return f"An error occurred while fetching products: {e}", 500
    finally:
        session.close()
    
    return render_template('home.html', pizzas=pizzas, drinks=drinks, desserts=desserts)

@app.route('/place_order', methods=['POST'])  # Updated route path and function name
def place_order():
    session = Session()
    try:
        customer_name = request.form.get('customer_name', 'Guest').strip()
        if not customer_name:
            customer_name = 'Guest'

        # Create a new Order
        new_order = Order(CustomerName=customer_name)
        session.add(new_order)
        session.commit()  # Commit to get the OrderID

        ordered_items = []

        # Process pizzas
        for pizza in session.query(Pizza).all():
            quantity_str = request.form.get(f'quantity_pizza_{pizza.PizzaID}', '0')
            try:
                quantity = int(quantity_str)
                if quantity < 0:
                    raise ValueError("Quantity cannot be negative.")
            except ValueError:
                return f"Invalid quantity for {pizza.Name}. Please enter a non-negative integer.", 400

            if quantity > 0:
                order_item = OrderItem(
                    OrderID=new_order.OrderID,
                    ItemTypeID=ItemType.PIZZA,  # Assuming ItemType.PIZZA is a string
                    ItemID=pizza.PizzaID,
                    Quantity=quantity,
                    Price=pizza.Price
                )
                session.add(order_item)
                ordered_items.append((pizza, quantity))
        
        # Process drinks
        for drink in session.query(Drink).all():
            quantity_str = request.form.get(f'quantity_drink_{drink.DrinkID}', '0')
            try:
                quantity = int(quantity_str)
                if quantity < 0:
                    raise ValueError("Quantity cannot be negative.")
            except ValueError:
                return f"Invalid quantity for {drink.Name}. Please enter a non-negative integer.", 400

            if quantity > 0:
                order_item = OrderItem(
                    OrderID=new_order.OrderID,
                    ItemTypeID=ItemType.DRINK,  # Assuming ItemType.DRINK is a string
                    ItemID=drink.DrinkID,
                    Quantity=quantity,
                    Price=drink.Price
                )
                session.add(order_item)
                ordered_items.append((drink, quantity))
        
        # Process desserts
        for dessert in session.query(Dessert).all():
            quantity_str = request.form.get(f'quantity_dessert_{dessert.DessertID}', '0')
            try:
                quantity = int(quantity_str)
                if quantity < 0:
                    raise ValueError("Quantity cannot be negative.")
            except ValueError:
                return f"Invalid quantity for {dessert.Name}. Please enter a non-negative integer.", 400

            if quantity > 0:
                order_item = OrderItem(
                    OrderID=new_order.OrderID,
                    ItemTypeID=ItemType.DESSERT,  # Assuming ItemType.DESSERT is a string
                    ItemID=dessert.DessertID,
                    Quantity=quantity,
                    Price=dessert.Price
                )
                session.add(order_item)
                ordered_items.append((dessert, quantity))
        
        session.commit()

        # Calculate total cost
        total_cost = sum(float(item.Price) * qty for item, qty in ordered_items)

        return render_template('order_confirmation.html', ordered_items=ordered_items, customer_name=customer_name, total_cost=total_cost)
    except Exception as e:
        session.rollback()
        return f"An error occurred while placing your order: {e}", 500
    finally:
        session.close()

if __name__ == '__main__':
    threading.Timer(1, open_browser).start()
    app.run(debug=True)
