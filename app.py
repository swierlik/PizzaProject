import sys
import os
from flask import Flask, render_template, request, redirect, url_for, flash, session as flask_session, jsonify
from sqlalchemy.orm import scoped_session, sessionmaker
import threading
import webbrowser
from functools import wraps
import datetime

from models.Order import Order
from models.OrderItem import OrderItem
from models.Item import Item
from models.Customer import Customer
from models.DiscountCode import DiscountCode
from Customers.CustomersManagement import attempt_login, add_customer
from Orders.OrdersManagement import (
    get_order_items,
    order_items_to_list,
    place_order,
    get_order,
    can_cancel_order,
    get_order_by_customer,
    refresh_orders_status
)

project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from db import Base, engine, SessionLocal

db_session = scoped_session(sessionmaker(bind=engine))

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

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
        pizzas = db_session.query(Item).filter_by(ItemType='PIZZA').all()
        drinks = db_session.query(Item).filter_by(ItemType='DRINK').all()
        desserts = db_session.query(Item).filter_by(ItemType='DESSERT').all()
    except Exception as e:
        return f"An error occurred while fetching products: {e}", 500

    return render_template('home.html', pizzas=pizzas[1:], drinks=drinks[1:], desserts=desserts)

@app.route('/apply_discount', methods=['POST'])
@login_required
def apply_discount():
    discount_code = request.form.get('discount_code')
    if discount_code:
        discount = db_session.query(DiscountCode).filter_by(Code=discount_code).first()
        if discount and not discount.IsRedeemed and discount.ExpiryDate >= datetime.datetime.now().date():
            flask_session['discount_code'] = discount_code
            return jsonify({'valid': True})
        else:
            return jsonify({'valid': False})
    else:
        return jsonify({'valid': False})

@app.route('/place_order', methods=['POST'])
@login_required
def place_order_route():
    try:
        customer_id = flask_session.get('customer_id')
        customer_name = flask_session.get('customer_name')
        discount_code = flask_session.get('discount_code')

        pizzas = {}
        drinks = {}
        desserts = {}

        for item in db_session.query(Item).filter_by(ItemType='PIZZA').all():
            quantity = int(request.form.get(f'quantity_pizza_{item.ItemID}', 0))
            if quantity > 0:
                pizzas[item.ItemID] = quantity

        for item in db_session.query(Item).filter_by(ItemType='DRINK').all():
            quantity = int(request.form.get(f'quantity_drink_{item.ItemID}', 0))
            if quantity > 0:
                drinks[item.ItemID] = quantity

        for item in db_session.query(Item).filter_by(ItemType='DESSERT').all():
            quantity = int(request.form.get(f'quantity_dessert_{item.ItemID}', 0))
            if quantity > 0:
                desserts[item.ItemID] = quantity

        if not (pizzas or drinks or desserts):
            flash("You didn't order anything!")
            return redirect(url_for('home'))
        
        if not pizzas:
            flash("You must order at least one pizza!")
            return redirect(url_for('home'))

        new_order, total_cost_before_discount, discount_amount = place_order(
            customer_id=customer_id,
            order_date=datetime.datetime.now(),
            pizzas=pizzas,
            drinks=drinks,
            desserts=desserts,
            discountCode=discount_code
        )

        order_items = get_order_items(new_order.OrderID)
        ordered_items = order_items_to_list(order_items, db_session)

        flask_session.pop('discount_code', None)

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
        refresh_orders_status()
        customer_id = flask_session.get('customer_id')
        customer_name = flask_session.get('customer_name')

        orders_list = get_order_by_customer(customer_id)

        # Pass the functions to the template
        return render_template(
            'orders.html',
            orders=orders_list,
            customer_name=customer_name,
            can_cancel_order=can_cancel_order,
            get_order_items=get_order_items,
            order_items_to_list=order_items_to_list,
            db_session=db_session
        )
    
    except Exception as e:
        app.logger.error(f"Error fetching orders: {e}")
        return f"An error occurred while fetching your orders: {e}", 500


@app.route('/cancel_order/<int:order_id>', methods=['POST'])
@login_required
def cancel_order(order_id):
    try:
        customer_id = flask_session.get('customer_id')

        with SessionLocal() as session_db:
            order = session_db.query(Order).filter_by(OrderID=order_id, CustomerID=customer_id).first()
            if not order:
                flash("Order not found.")
                return redirect(url_for('orders'))

            if can_cancel_order(order_id):
                order.OrderStatus = "Canceled"
                session_db.commit()
                flash(f"Order {order_id} has been canceled successfully.")
            else:
                flash(f"Order {order_id} cannot be canceled (time window expired or already processed).")

        return redirect(url_for('orders'))
    
    except Exception as e:
        app.logger.error(f"Error canceling order {order_id}: {e}")
        flash("An error occurred while trying to cancel your order.")
        return redirect(url_for('orders'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    flask_session.clear()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        customer = db_session.query(Customer).filter_by(Username=username).first()
        if customer and attempt_login(username, password):  
            flask_session['customer_id'] = customer.CustomerID
            flask_session['customer_name'] = customer.Name
            flash('Logged in successfully.')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        gender = request.form.get('gender')
        birthdate = request.form.get('dob')
        phone_number = request.form.get('phone')
        address = request.form.get('address')
        postal_code = request.form.get('postal_code')

        existing_customer = db_session.query(Customer).filter_by(Username=username).first()
        if existing_customer:
            flash('Username already exists. Please choose a different one.')
            return redirect(url_for('register'))

        if birthdate:
            birthdate = datetime.datetime.strptime(birthdate, '%Y-%m-%d').date()

        created_at = datetime.datetime.now()

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
    flask_session.pop('customer_id', None)
    flask_session.pop('customer_name', None)
    flash('You have been logged out.')
    return redirect(url_for('home'))

if __name__ == '__main__':
    if not os.environ.get('WERKZEUG_RUN_MAIN'):
        threading.Timer(1, open_browser).start()
    app.run(debug=True)
