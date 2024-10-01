import sys
import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from sqlalchemy.orm import scoped_session, sessionmaker
import threading
import webbrowser
from functools import wraps
import datetime

# Add project root to sys.path to resolve imports
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import database session and Base
from db import Base, engine, create_all_tables

# Set up scoped_session
db_session = scoped_session(sessionmaker(bind=engine))

# Import Models
from models.Order import Order
from models.OrderItem import OrderItem
from Orders.ItemType import ItemType
from models.Pizza import Pizza
from models.Drink import Drink
from models.Dessert import Dessert
from models.Customer import Customer
from models.DiscountCode import DiscountCode
from Customers.CustomersManagement import attempt_login, add_customer
from Orders.OrdersManagement import place_order

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

# Decorator to require login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'customer_id' not in session:
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

@app.route('/apply_discount', methods=['POST'])
@login_required
def apply_discount():
    discount_code = request.form.get('discount_code')
    if discount_code:
        # Validate the discount code
        discount = db_session.query(DiscountCode).filter_by(Code=discount_code).first()
        if discount and not discount.IsRedeemed and discount.ExpiryDate >= datetime.datetime.now().date():
            # Store the discount code in the session
            session['discount_code'] = discount_code
            return jsonify({'valid': True})
        else:
            return jsonify({'valid': False})
    else:
        return jsonify({'valid': False})


@app.route('/place_order', methods=['POST'])
@login_required
def place_order_route():
    try:
        customer_id = session.get('customer_id')
        customer_name = session.get('customer_name')
        discount_code = session.get('discount_code')

        pizzas = {}
        drinks = {}
        desserts = {}

        # Collect quantities from form data
        for pizza in db_session.query(Pizza).all():
            quantity = int(request.form.get(f'quantity_pizza_{pizza.PizzaID}', 0))
            if quantity > 0:
                pizzas[pizza.PizzaID] = quantity

        for drink in db_session.query(Drink).all():
            quantity = int(request.form.get(f'quantity_drink_{drink.DrinkID}', 0))
            if quantity > 0:
                drinks[drink.DrinkID] = quantity

        for dessert in db_session.query(Dessert).all():
            quantity = int(request.form.get(f'quantity_dessert_{dessert.DessertID}', 0))
            if quantity > 0:
                desserts[dessert.DessertID] = quantity

        if not (pizzas or drinks or desserts):
            flash("You didn't order anything!")
            return redirect(url_for('home'))

        # Call the place_order function from OrdersManagement
        new_order = place_order(
            customer_id=customer_id,
            order_date=datetime.datetime.now(),
            pizzas=pizzas,
            drinks=drinks,
            desserts=desserts,
            discountCode=discount_code
        )

        # Remove the discount code from the session if it was used
        if discount_code and 'discount_code' in session:
            del session['discount_code']

        # Retrieve ordered items for confirmation
        ordered_items = db_session.query(OrderItem).filter_by(OrderID=new_order.OrderID).all()

        # Render the order confirmation template
        return render_template(
            'order_confirmation.html',
            ordered_items=ordered_items,
            customer_name=customer_name,
            total_cost=new_order.TotalPrice,
            estimated_time=new_order.EstimatedDeliveryTime
        )
    except Exception as e:
        db_session.rollback()
        app.logger.error(f"Error during order placement: {e}")
        return f"An error occurred while placing your order: {e}", 500


@app.route('/orders')
@login_required
def orders():
    try:
        customer_id = session.get('customer_id')

        customer = db_session.query(Customer).get(customer_id)
        orders = db_session.query(Order).filter_by(CustomerID=customer.CustomerID).all()

        order_details = []

        for order in orders:
            items = db_session.query(OrderItem).filter_by(OrderID=order.OrderID).all()
            item_list = []
            for item in items:
                if item.ItemTypeID == ItemType.PIZZA:
                    pizza = db_session.query(Pizza).get(item.ItemID)
                    item_name = pizza.Name
                elif item.ItemTypeID == ItemType.DRINK:
                    drink = db_session.query(Drink).get(item.ItemID)
                    item_name = drink.Name
                elif item.ItemTypeID == ItemType.DESSERT:
                    dessert = db_session.query(Dessert).get(item.ItemID)
                    item_name = dessert.Name
                else:
                    item_name = 'Unknown Item'

                item_list.append({'name': item_name, 'quantity': item.Quantity})

            order_details.append({'order': order, 'items': item_list})

        return render_template('orders.html', order_details=order_details)
    except Exception as e:
        app.logger.error(f"Error fetching orders: {e}")
        return f"An error occurred while fetching your orders: {e}", 500

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Retrieve form data
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Authenticate user
        customer = db_session.query(Customer).filter_by(Username=username).first()
        if customer and attempt_login(username, password):  
            session['customer_id'] = customer.CustomerID
            session['customer_name'] = customer.Name
            flash('Logged in successfully.')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Check if username already exists
        existing_customer = db_session.query(Customer).filter_by(Username=username).first()
        if existing_customer:
            flash('Username already exists. Please choose a different one.')
            return redirect(url_for('register'))
        
        # Create new customer using the add_customer class method
        new_customer = add_customer(name=name, username=username, password=password)
        
        flash('Registration successful. Please log in.')
        return redirect(url_for('login'))
    
    return render_template('register.html')
@app.route('/logout')
def logout():
    # Remove user information from the session
    session.pop('customer_id', None)
    session.pop('customer_name', None)
    flash('You have been logged out.')
    return redirect(url_for('home'))

# Optional: Route to list all endpoints for debugging
@app.route('/routes')
def list_routes():
    output = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(sorted(rule.methods))
        try:
            url = url_for(rule.endpoint, **(rule.defaults or {}))
        except Exception:
            url = "Unresolvable URL"
        line = f"{rule.endpoint:30s} {methods:25s} {url}"
        output.append(line)
    return "<pre>" + "\n".join(sorted(output)) + "</pre>"

if __name__ == '__main__':

    threading.Timer(1, open_browser).start()
    app.run(debug=True)
