from models.Item import Item
from db import session

def add_drink(name, price):
    new_drink = Item(
        ItemType='DRINK',
        Name=name,
        Price=price
    )
    session.add(new_drink)
    session.commit()
    print(f"Drink '{name}' added to the database.")

def get_price_drink(drinkID):
    drink = session.query(Item).filter(Item.ItemID == drinkID, Item.ItemType == 'DRINK').first()
    return float(drink.Price)

def add_dessert(name, price):
    new_dessert = Item(
        ItemType='DESSERT',
        Name=name,
        Price=price
    )
    session.add(new_dessert)
    session.commit()
    print(f"Dessert '{name}' added to the database.")

def get_price_dessert(dessertID):
    dessert = session.query(Item).filter(Item.ItemID == dessertID, Item.ItemType == 'DESSERT').first()
    return float(dessert.Price)
