from sqlalchemy import Boolean, Column, Integer, String, Numeric
from db import Base, session

class Ingredient(Base):
    __tablename__ = 'Ingredient'

    IngredientID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(255), nullable=False)
    Cost = Column(Numeric, nullable=False)
    isVegetarian = Column(Boolean, default=False)
    isVegan = Column(Boolean, default=False)

    def __repr__(self):
        return (f"<Ingredient(IngredientID={self.IngredientID}, Name='{self.Name}', Cost={self.Cost})>")

# Function to add an ingredient
def add_ingredient(name, cost, is_vegetarian=False, is_vegan=False):
    new_ingredient = Ingredient(
        Name=name,
        Cost=cost,
        isVegetarian=is_vegetarian,
        isVegan=is_vegan
    )
    session.add(new_ingredient)
    session.commit()
    print(f"Ingredient '{name}' added to the database.")

def get_price(ingredient_id):
    ingredient = session.query(Ingredient).filter(Ingredient.IngredientID == ingredient_id).first()
    return ingredient.Cost

def is_vegetarian(ingredient_id):
    ingredient = session.query(Ingredient).filter(Ingredient.IngredientID == ingredient_id).first()
    return ingredient.isVegetarian

def is_vegan(ingredient_id):
    ingredient = session.query(Ingredient).filter(Ingredient.IngredientID == ingredient_id).first()
    return ingredient.isVegan

