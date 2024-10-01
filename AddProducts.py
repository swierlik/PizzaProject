# AddProducts.py

from datetime import datetime
from Customers.CustomersManagement import add_customer, add_discount_code
from Orders.OrdersManagement import place_order
from Products.ExtrasManagement import add_dessert, add_drink
from Products.PizzaManagement import add_pizza
from Products.IngredientManagement import add_ingredient


# Add drinks
add_drink("Coke", 1.99)
add_drink("Sprite", 1.99)

# Add desserts
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
add_ingredient("Banana", 0.75, is_vegetarian=True, is_vegan=True)
add_ingredient("Strawberry", 0.75, is_vegetarian=True, is_vegan=True)
add_ingredient("Nutella", 0.75, is_vegetarian=True, is_vegan=False)

# Add pizzas
add_pizza("Margherita", "Tomato, cheese, basil", [1, 2, 3, 8, 11])
add_pizza("Pepperoni", "Tomato, cheese, pepperoni", [1, 2, 3, 4, 8, 11])
add_pizza("Vegetarian", "Tomato, cheese, mushrooms, olives, pineapple, onion, garlic, basil, oregano", [1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])
add_pizza("Hawaiian", "Tomato, cheese, ham, pineapple", [1, 2, 3, 17, 7])
add_pizza("Meat Feast", "Tomato, cheese, pepperoni, ham, chicken, beef", [1, 2, 3, 4, 17, 18, 19])
add_pizza("Vegan", "Tomato, vegan cheese, mushrooms, olives, pineapple, onion, garlic, basil, oregano", [1, 2, 20, 5, 6, 7, 8, 9, 10, 11, 12, 13])
add_pizza("Spicy", "Tomato, cheese, pepperoni, chilli flakes, pepper", [1, 2, 3, 4, 13, 14])
add_pizza("Cheese Feast", "Tomato, cheese, vegan cheese", [1, 2, 3, 20])
add_pizza("Dessert", "Nutella, banana, strawberry", [1, 21, 22, 23])
add_pizza("Fruity", "Tomato, cheese, pineapple, banana, strawberry", [1, 2, 3, 7, 21, 22])

# Add discount codes
add_discount_code("DISCOUNT10", "10% off your order", "2025-12-31", 10)
add_discount_code("DISCOUNT20", "20% off your order", "2025-12-31", 20)
add_discount_code("DISCOUNT50", "50% off your order", "2025-12-31", 50)


#Add a customer
add_customer(username = "1", password = "123", name="One")
add_customer(username = "2", password = "123", name="Two")
add_customer(username = "3", password = "123", name="Three")
add_customer(username = "4", password = "123", name="Four")

#Add some orders
place_order(1, datetime.now(), {1: 1, 2: 2}, {1: 1}, {1: 1}, "DISCOUNT10")
place_order(1, datetime.now(), {3: 1, 4: 1}, {2: 2}, {2: 1}, "DISCOUNT20")
place_order(3, datetime.now(), {5: 1, 6: 1}, {1: 1}, {3: 1}, "DISCOUNT50")