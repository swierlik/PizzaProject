# main.py
from db import create_all_tables  # This should work if `db.py` is in the same directory as `AddProducts.py`

from products.pizza import add_pizza
from products.drink import add_drink
from products.dessert import add_dessert
from db import create_all_tables


# Create all tables in the database
create_all_tables()

# Add pizzas
add_pizza("Margherita", "Classic delight with 100% real mozzarella cheese", 8.99, is_vegetarian=True, is_vegan=False)
add_pizza("Pepperoni", "Pepperoni and cheese", 9.99, is_vegetarian=False, is_vegan=False)

# Add drinks
add_drink("Coke", 1.99)
add_drink("Sprite", 1.99)

# Add dessertsS
add_dessert("Chocolate Cake", 5.00)
add_dessert("Ice Cream", 3.50)
