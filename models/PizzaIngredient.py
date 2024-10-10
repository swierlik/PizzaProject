from sqlalchemy import Column, Integer, ForeignKey
from database import Base

class PizzaIngredient(Base):
    __tablename__ = 'pizza_ingredients'

    PizzaID = Column(Integer, ForeignKey('pizzas.PizzaID'), primary_key=True, autoincrement=True)
    IngredientID = Column(Integer, ForeignKey('ingredients.IngredientID'), primary_key=True)

    def __repr__(self):
        return f"<PizzaIngredient(PizzaID={self.PizzaID}, IngredientID={self.IngredientID})>"



