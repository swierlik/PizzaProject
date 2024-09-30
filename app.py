# app.py

import sys
import os
from flask import Flask, render_template, request, redirect, url_for, flash, session as flask_session
from sqlalchemy.orm import scoped_session, sessionmaker
import threading
import webbrowser
from functools import wraps

# Add project root to sys.path to resolve imports
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import database session and Base
from db import Base, engine, create_all_tables

# Set up scoped_session
db_session = scoped_session(sessionmaker(bind=engine))

# Import Models
from Orders.Order import Order
from Orders.OrderItem import OrderItem
from Orders.ItemType import ItemType
from products.pizza import Pizza
from products.drink import Drink
from products.dessert import Dessert

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

# Decorator to require login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'customer_id' not in flask_session:
            flash('Please log in to access this page.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/')
@login_required
def home():
    try:
        # Retrieve products from the database
        pizzas = db_session.query(Pizza).all()
        drinks = db_session.query(Drink).all()
        desserts = db_session.query(Dessert).all()
    except Exception as e:
        return f"An error occurred while fetching products: {e}", 500

    return render_template('home.html', pizzas=pizzas, drinks=drinks, desserts=desserts)

@app.route('/register', methods=['GET', 'POST'])
def register():
    from Customer.customer import Customer

    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            name = request.form['name']

            # Check if the username already exists
            existing_user = db_session.query(Customer).filter_by(Username=username).first()
            if existing_user:
                flash('Username already exists. Please choose a different one.')
                return redirect(url_for('register'))

            # Create a new customer using the class method
            new_customer = Customer.add_customer(db_session, name=name, username=username, password=password)
            db_session.commit()
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
        except Exception as e:
            db_session.rollback()
            app.logger.error(f"Error during registration: {e}")
            flash('An error occurred during registration. Please try again.')
            return redirect(url_for('register'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    from Customer.customer import Customer

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        customer = db_session.query(Customer).filter_by(Username=username).first()
        if customer and customer.Password == Customer.hash_password(password):
            flask_session['customer_id'] = customer.CustomerID
            flask_session['customer_name'] = customer.Name
            flash('Logged in successfully!')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    flask_session.clear()
    flash('You have been logged out.')
    return redirect(url_for('home'))

@app.route('/place_order', methods=['POST'])
@login_required
def place_order():
    try:
        customer_id = flask_session.get('customer_id')
        customer_name = flask_session.get('customer_name')
        from Customer.customer import Customer

        customer = db_session.query(Customer).get(customer_id)

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
                order_item = OrderItem.add_order_item(
                    db_session,
                    order_id=new_order.OrderID,
                    item_type_id=ItemType.PIZZA,
                    item_id=pizza.PizzaID,
                    quantity=quantity
                )
                ordered_items.append((pizza, quantity))
                total_cost += float(pizza.Price) * quantity

        # Process drinks
        for drink in db_session.query(Drink).all():
            quantity_str = request.form.get(f'quantity_drink_{drink.DrinkID}', '0')
            quantity = int(quantity_str) if quantity_str.isdigit() else 0

            if quantity > 0:
                order_item = OrderItem.add_order_item(
                    db_session,
                    order_id=new_order.OrderID,
                    item_type_id=ItemType.DRINK,
                    item_id=drink.DrinkID,
                    quantity=quantity
                )
                ordered_items.append((drink, quantity))
                total_cost += float(drink.Price) * quantity

        # Process desserts
        for dessert in db_session.query(Dessert).all():
            quantity_str = request.form.get(f'quantity_dessert_{dessert.DessertID}', '0')
            quantity = int(quantity_str) if quantity_str.isdigit() else 0

            if quantity > 0:
                order_item = OrderItem.add_order_item(
                    db_session,
                    order_id=new_order.OrderID,
                    item_type_id=ItemType.DESSERT,
                    item_id=dessert.DessertID,
                    quantity=quantity
                )
                ordered_items.append((dessert, quantity))
                total_cost += float(dessert.Price) * quantity

        if not ordered_items:
            flash("You didn't order anything!")
            return redirect(url_for('home'))

        # Update the total price in the order
        new_order.TotalPrice = total_cost
        db_session.commit()

        # Estimated time (for example purposes, we set it to 30 minutes)
        estimated_time = 30

        return render_template('order_confirmation.html', ordered_items=ordered_items, customer_name=customer_name, total_cost=total_cost, estimated_time=estimated_time)
    except Exception as e:
        db_session.rollback()
        app.logger.error(f"Error during order placement: {e}")
        return f"An error occurred while placing your order: {e}", 500

if __name__ == '__main__':
    create_all_tables()  # Create tables if they don't exist
    threading.Timer(1, open_browser).start()
    app.run(debug=True)
