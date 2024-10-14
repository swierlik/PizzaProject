# AddProducts.py

from datetime import datetime, timedelta
from Customers.CustomersManagement import add_customer, add_discount_code
from Deliveries.DeliveryManagement import add_delivery_person
from Orders.OrdersManagement import place_order
from Products.ExtrasManagement import add_dessert, add_drink
from Products.PizzaManagement import add_pizza
from Products.IngredientManagement import add_ingredient
from models.Order import Order


# Add drinks
add_drink("Birthday Drink", 0.00)
add_drink("Coke", 1.99)
add_drink("Sprite", 1.99)
add_drink("Fanta", 1.99)
add_drink("Water", 0.99)

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

add_pizza("Birthday Pizza", [1, 2, 3, 17], set_price=0.00)
add_pizza("Margherita", [1, 2, 3, 8, 11])
add_pizza("Pepperoni", [1, 2, 3, 4, 8, 11])
add_pizza("Vegetarian", [1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])
add_pizza("Hawaiian", [1, 2, 3, 17, 7])
add_pizza("Meat Feast", [1, 2, 3, 4, 17, 18, 19])
add_pizza("Vegan", [1, 2, 20, 5, 6, 7, 8, 9, 10, 11, 12, 13])
add_pizza("Spicy", [1, 2, 3, 4, 13, 14])
add_pizza("Cheese Feast", [1, 2, 3, 20])
add_pizza("Dessert", [1, 21, 22, 23])
add_pizza("Fruity", [1, 2, 3, 7, 21, 22])




# Add discount codes
add_discount_code("DISCOUNT10", "10% off your order", "2025-12-31", 10)
add_discount_code("DISCOUNT20", "20% off your order", "2025-12-31", 20)
add_discount_code("DISCOUNT50", "50% off your order", "2025-12-31", 50)
add_discount_code("ILIKEMEN", "100% off for legends", "2025-12-31", 100)

#Add a delivery person
add_delivery_person(name="John", postal_code="E1 1AA")
add_delivery_person(name="Jane", postal_code="E1 1AB")
add_delivery_person(name="Jack", postal_code="E1 1AC")
add_delivery_person(name="Jill", postal_code="E1 1AA")
add_delivery_person(name="James", postal_code="E1 1AB")
add_delivery_person(name="Jenny", postal_code="E1 1AC")
add_delivery_person(name="Joe", postal_code="E1 1AA")
add_delivery_person(name="Wen Xiao Huang", postal_code="E1 1AB")


#Add a customer
add_customer(username = "1", password = "123", name="One", postal_code="E1 1AA")
add_customer(username = "2", password = "123", name="Two", postal_code="E1 1AA")

#FOR TESTING PURPOSES

# #Add a customer
# add_customer(username = "1", password = "123", name="One", postal_code="E1 1AA")
# add_customer(username = "2", password = "123", name="Two", postal_code="E1 1AB")
# add_customer(username = "3", password = "123", name="Three", postal_code="E1 1AC")
# add_customer(username = "4", password = "123", name="Four", postal_code="E1 1AD")

