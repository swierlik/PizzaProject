from sqlalchemy import Column, Integer, ForeignKey
from db import Base, session

class PizzaIngredient(Base):
    __tablename__ = 'PizzaIngredient'

    PizzaID = Column(Integer, ForeignKey('Pizza.PizzaID'), primary_key=True, autoincrement=True)
    IngredientID = Column(Integer, ForeignKey('Ingredient.IngredientID'), primary_key=True)

    def __repr__(self):
        return f"<PizzaIngredient(PizzaID={self.PizzaID}, IngredientID={self.IngredientID})>"

# Function to add a pizza ingredient
def add_pizza_ingredient(pizza_id, ingredient_id):
    new_pizza_ingredient = PizzaIngredient(
        PizzaID=pizza_id,
        IngredientID=ingredient_id
    )
    session.add(new_pizza_ingredient)
    session.commit()
    print(f"PizzaIngredient for PizzaID '{pizza_id}' and IngredientID '{ingredient_id}' added to the database.")

