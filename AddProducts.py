# main.py
from db import create_all_tables  # This should work if `db.py` is in the same directory as `AddProducts.py`

from products.pizza import add_pizza
from products.drink import add_drink
from products.dessert import add_dessert
from products.ingredient import add_ingredient
from db import create_all_tables


# Create all tables in the database
create_all_tables()

# Add drinks
add_drink("Coke", 1.99)
add_drink("Sprite", 1.99)

# Add dessertsS
add_dessert("Chocolate Cake", 5.00)
add_dessert("Ice Cream", 3.50)
add_dessert("Cheesecake", 4.50)
add_dessert("Tiramisu", 4.50)
add_dessert("Panna Cotta", 4.50)

# Add ingredients to the database
add_ingredient("Base", 2.00, is_vegetarian=True, is_vegan=True)
add_ingredient("Cheese", 0.50, is_vegetarian=True, is_vegan=False)
add_ingredient("Sauce", 0.50, is_vegetarian=True, is_vegan=True)
add_ingredient("Pepperoni", 1.00, is_vegetarian=False, is_vegan=False)
add_ingredient("Mushrooms", 0.75, is_vegetarian=True, is_vegan=True)
add_ingredient("Olives", 0.75, is_vegetarian=True, is_vegan=True)
add_ingredient("Pineapple", 0.75, is_vegetarian=True, is_vegan=True)
add_ingredient("Tomato", 0.50, is_vegetarian=True, is_vegan=True)
add_ingredient("Onion", 0.50, is_vegetarian=True, is_vegan=True)
add_ingredient("Garlic", 0.50, is_vegetarian=True, is_vegan=True)
add_ingredient("Basil", 0.50, is_vegetarian=True, is_vegan=True)
add_ingredient("Oregano", 0.50, is_vegetarian=True, is_vegan=True)
add_ingredient("Chilli Flakes", 0.50, is_vegetarian=True, is_vegan=True)
add_ingredient("Pepper", 0.50, is_vegetarian=True, is_vegan=True)
add_ingredient("Salt", 0.50, is_vegetarian=True, is_vegan=True)
add_ingredient("Sugar", 0.50, is_vegetarian=True, is_vegan=True)
add_ingredient("Ham", 1.00, is_vegetarian=False, is_vegan=False)
add_ingredient("Chicken", 1.00, is_vegetarian=False, is_vegan=False)
add_ingredient("Beef", 1.00, is_vegetarian=False, is_vegan=False)
add_ingredient("Vegan Cheese", 1.00, is_vegetarian=True, is_vegan=True)

## Add pizzas
add_pizza("Margherita", "Tomato, cheese, basil", [1, 2, 3, 8, 11])
add_pizza("Pepperoni", "Tomato, cheese, pepperoni", [1, 2, 3, 4, 8, 11])
add_pizza("Vegetarian", "Tomato, cheese, mushrooms, olives, pineapple, tomato, onion, garlic, basil, oregano", [1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])
add_pizza("Hawaiian", "Tomato, cheese, ham, pineapple", [1, 2, 3, 17, 7])
add_pizza("Meat Feast", "Tomato, cheese, pepperoni, ham, chicken, beef", [1, 2, 3, 4, 17, 18, 19])
add_pizza("Vegan", "Tomato, vegan cheese, mushrooms, olives, pineapple, tomato, onion, garlic, basil, oregano", [1, 2, 20, 5, 6, 7, 8, 9, 10, 11, 12, 13])




