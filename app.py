import sys
import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from sqlalchemy import select
from sqlalchemy.orm import scoped_session, sessionmaker, joinedload
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
from Orders.OrdersManagement import get_orders_by_customer, place_order

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

        # Call the place_order function
        new_order, total_cost_before_discount, discount_amount = place_order(
            customer_id=customer_id,
            order_date=datetime.datetime.now(),
            pizzas=pizzas,
            drinks=drinks,
            desserts=desserts,
            discountCode=discount_code
        )

        # Retrieve ordered items for confirmation
        ordered_items = db_session.query(OrderItem).filter_by(OrderID=new_order.OrderID).all()

        # Render the order confirmation template
        return render_template(
            'order_confirmation.html',
            ordered_items=ordered_items,
            customer_name=customer_name,
            total_cost=new_order.TotalPrice,
            total_cost_before_discount=total_cost_before_discount,
            discount_amount=discount_amount,
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

        orders = customer.orders
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(type(orders))

        order_details = []

        for order in orders:
            items = order.order_items

            if items is None:
                app.logger.warning(f"No items found for order ID {order.OrderID}")
                continue  # Skip if there are no items

            item_list = []
            for item in items:
                item_name = 'Unknown Item'
                if item.ItemTypeID == ItemType.PIZZA:
                    pizza = db_session.execute(select(Pizza).where(Pizza.PizzaID == item.ItemID)).scalars().first()
                    item_name = pizza.Name if pizza else 'Unknown Item'
                elif item.ItemTypeID == ItemType.DRINK:
                    drink = db_session.execute(select(Drink).where(Drink.DrinkID == item.ItemID)).scalars().first()
                    item_name = drink.Name if drink else 'Unknown Item'
                elif item.ItemTypeID == ItemType.DESSERT:
                    dessert = db_session.execute(select(Dessert).where(Dessert.DessertID == item.ItemID)).scalars().first()
                    item_name = dessert.Name if dessert else 'Unknown Item'

                item_list.append({'name': item_name, 'quantity': item.Quantity})

            order_details.append({'order': order, 'items': item_list})

        return render_template('orders.html', order_details=order_details)
    except Exception as e:
        app.logger.error(f"Error fetching orders: {e}")
        return f"An error occurred while fetching your orders: {e}", 500


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        gender = request.form.get('gender')
        birthdate = request.form.get('dob')  # Date of Birth from date picker
        phone_number = request.form.get('phone')
        address = request.form.get('address')
        postal_code = request.form.get('postal_code')
        
        # Check if username already exists
        existing_customer = db_session.query(Customer).filter_by(Username=username).first()
        if existing_customer:
            flash('Username already exists. Please choose a different one.')
            return redirect(url_for('register'))
        
        # Convert birthdate string to a date object
        if birthdate:
            birthdate = datetime.datetime.strptime(birthdate, '%Y-%m-%d').date()
        
        # Add a timestamp for when the customer is created
        created_at = datetime.datetime.now()

        # Create new customer using the add_customer method
        add_customer(
            name=name,
            username=username,
            password=password,
            gender=gender,
            birthdate=birthdate,
            phone_number=phone_number,
            address=address,
            postal_code=postal_code,
            created_at=created_at
        )
        
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
    
    if not os.environ.get('WERKZEUG_RUN_MAIN'):  # Check if the reloader process is running
        threading.Timer(1, open_browser).start()
    app.run(debug=True)

