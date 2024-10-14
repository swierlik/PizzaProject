from sqlalchemy import Boolean, Column, Integer, String, Numeric
from database import Base

class Ingredient(Base):
    __tablename__ = 'ingredients'

    IngredientID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(255), nullable=False)
    Price = Column(Numeric, nullable=False)
    IsVegetarian = Column(Boolean, default=False)
    IsVegan = Column(Boolean, default=False)

    def __repr__(self):
        return (f"<Ingredient(IngredientID={self.IngredientID}, Name='{self.Name}', Price={self.Price})>")
