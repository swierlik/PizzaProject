from Products.IngredientManagement import get_price_ingredient, is_vegan_ingredient, is_vegetarian_ingredient
from models.Ingredient import Ingredient
from models.ItemIngredient import ItemIngredient
from models.Item import Item
from db import session
from sqlalchemy.exc import SQLAlchemyError

def add_pizza(name, ingredients, description_preset=None, set_price=999):
    try:
        price = 0.0
        all_ingredients_vegetarian = True
        all_ingredients_vegan = True
        description = ""

        for ingredient_id in ingredients:
            price += get_price_ingredient(ingredient_id)
            description += f'{get_ingredient_name(ingredient_id)}, '
            if not is_vegetarian_ingredient(ingredient_id):
                all_ingredients_vegetarian = False
            if not is_vegan_ingredient(ingredient_id):
                all_ingredients_vegan = False

        if description_preset:
            description = description_preset
        
        price *= 1.40 * 1.09  # 40% profit margin and 9% tax
        if set_price != 999:
            price = set_price

        new_item = Item(
            ItemType='PIZZA',
            Name=name,
            Description=description,
            Price=price,
            IsVegetarian=all_ingredients_vegetarian,  
            IsVegan=all_ingredients_vegan  
        )
        session.add(new_item)
        session.commit()

        pizza_id = new_item.ItemID

        for ingredient_id in ingredients:
            session.add(make_pizza_ingredient(pizza_id, ingredient_id))

        session.commit()
        print(f"Pizza '{name}' added to the database with ingredients.")
    
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error occurred: {e}")

def make_pizza_ingredient(pizza_id, ingredient_id):
    new_pizza_ingredient = ItemIngredient(
        ItemID=pizza_id,
        IngredientID=ingredient_id
    )
    return new_pizza_ingredient

def get_ingredient_name(ingredientID):
    ingredient = session.query(Ingredient).filter(Ingredient.IngredientID == ingredientID).first()
    return ingredient.Name
