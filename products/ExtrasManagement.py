from models.Drink import Drink
from models.Dessert import Dessert
from db import session

##DRINKS
def add_drink(name, price):
    new_drink = Drink(
        Name=name,
        Price=price
    )
    session.add(new_drink)
    session.commit()
    print(f"Drink '{name}' added to the database.")

def get_price_drink(drinkID):
    drink = session.query(Drink).filter(Drink.DrinkID == drinkID).first()
    return float(drink.Price)


##DESSERTS
def add_dessert(name, price):
    new_dessert = Dessert(
        Name=name,
        Price=price
    )
    session.add(new_dessert)
    session.commit()
    print(f"Dessert '{name}' added to the database.")

def get_price_dessert(dessertID):
    dessert = session.query(Dessert).filter(Dessert.DessertID == dessertID).first()
    return float(dessert.Price)


