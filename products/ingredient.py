from sqlalchemy import Column, Integer, String, Numeric
from db import Base, session

class Ingredient(Base):
    __tablename__ = 'Ingredient'

    IngredientID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(255), nullable=False)
    Cost = Column(Numeric, nullable=False)

    def __repr__(self):
        return (f"<Ingredient(IngredientID={self.IngredientID}, Name='{self.Name}', Cost={self.Cost})>")

# Function to add an ingredient
def add_ingredient(name, cost):
    new_ingredient = Ingredient(
        Name=name,
        Cost=cost
    )
    session.add(new_ingredient)
    session.commit()
    print(f"Ingredient '{name}' added to the database.")

