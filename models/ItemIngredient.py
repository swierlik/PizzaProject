from sqlalchemy import Column, Integer, ForeignKey
from database import Base

class ItemIngredient(Base):
    __tablename__ = 'item_ingredients'

    ItemID = Column(Integer, ForeignKey('items.ItemID'), primary_key=True)
    IngredientID = Column(Integer, ForeignKey('ingredients.IngredientID'), primary_key=True)

    def __repr__(self):
        return f"<ItemIngredient(ItemID={self.ItemID}, IngredientID={self.IngredientID})>"
