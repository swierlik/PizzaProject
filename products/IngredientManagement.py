from models.Ingredient import Ingredient
from db import session


# Function to add an ingredient
def add_ingredient(name, price, is_vegetarian=False, is_vegan=False):
    new_ingredient = Ingredient(
        Name=name,
        Price=price,
        IsVegetarian=is_vegetarian,
        IsVegan=is_vegan
    )
    session.add(new_ingredient)
    session.commit()
    print(f"Ingredient '{name}' added to the database.")

def get_price_ingredient(ingredientID):
    ingredient = session.query(Ingredient).filter(Ingredient.IngredientID == ingredientID).first()
    return float(ingredient.Price)

def is_vegetarian_ingredient(ingredientID):
    ingredient = session.query(Ingredient).filter(Ingredient.IngredientID == ingredientID).first()
    return ingredient.IsVegetarian

def is_vegan_ingredient(ingredientID):
    ingredient = session.query(Ingredient).filter(Ingredient.IngredientID == ingredientID).first()
    return ingredient.IsVegan