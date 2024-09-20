from sqlalchemy import Column, Integer, ForeignKey, DECIMAL, String
from sqlalchemy.orm import relationship
from db import Base, session

# Define the ItemType Enum


class ItemType:
    PIZZA = 'PIZZA'
    DRINK = 'DRINK'
    DESSERT = 'DESSERT'
