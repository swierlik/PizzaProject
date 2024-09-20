# app.py
from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import threading
import webbrowser

from db import Base, engine

from products.pizza import Pizza
from products.drink import Drink
from products.dessert import Dessert
from models import Order, OrderItem  # Assuming you have these models defined
from item_types import ItemType  # Enum for item types

app = Flask(__name__)

# Database configuration
engine = create_engine('sqlite:///pizzeria.db')  # Update with your database URL
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

def open_browser():
    webbrowser.open_new('http://127.0.0.1:5000/')

@app.route('/')
def home():
    # Retrieve products from the database
    pizzas = session.query(Pizza).all()
    drinks = session.query(Drink).all()
    desserts = session.query(Dessert).all()
    
    return render_template('home.html', pizzas=pizzas, drinks=drinks, desserts=desserts)

@app.route('/order', methods=['POST'])
def order():
    customer_name = request.form.get('customer_name', 'Guest')

    # Create a new Order
    new_order = Order(CustomerName=customer_name)
    session.add(new_order)
    session.commit()  # Commit to get the OrderID

    ordered_items = []

    # Process pizzas
    for pizza in session.query(Pizza).all():
        quantity = int(request.form.get(f'quantity_pizza_{pizza.PizzaID}', 0))
        if quantity > 0:
            order_item = OrderItem(
                OrderID=new_order.OrderID,
                ItemTypeID=ItemType.PIZZA.value,
                ItemID=pizza.PizzaID,
                Quantity=quantity,
                Price=pizza.Price
            )
            session.add(order_item)
            ordered_items.append((pizza, quantity))
    
    # Process drinks
    for drink in session.query(Drink).all():
        quantity = int(request.form.get(f'quantity_drink_{drink.DrinkID}', 0))
        if quantity > 0:
            order_item = OrderItem(
                OrderID=new_order.OrderID,
                ItemTypeID=ItemType.DRINK.value,
                ItemID=drink.DrinkID,
                Quantity=quantity,
                Price=drink.Price
            )
            session.add(order_item)
            ordered_items.append((drink, quantity))
    
    # Process desserts
    for dessert in session.query(Dessert).all():
        quantity = int(request.form.get(f'quantity_dessert_{dessert.DessertID}', 0))
        if quantity > 0:
            order_item = OrderItem(
                OrderID=new_order.OrderID,
                ItemTypeID=ItemType.DESSERT.value,
                ItemID=dessert.DessertID,
                Quantity=quantity,
                Price=dessert.Price
            )
            session.add(order_item)
            ordered_items.append((dessert, quantity))
    
    session.commit()

    return render_template('order_confirmation.html', ordered_items=ordered_items, customer_name=customer_name)

if __name__ == '__main__':
    threading.Timer(1, open_browser).start()
    app.run()
