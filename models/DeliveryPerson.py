from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from database import Base

class DeliveryPerson(Base):
    __tablename__ = 'delivery_persons'  # Plural table name 'delivery_persons'

    DeliveryPersonID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(255), nullable=False)
    PostalCode = Column(String(255))
    IsAvailable = Column(Boolean, default=True)

    # Relationships
    assigned_orders = relationship('Order', back_populates='delivery_person')

    def __repr__(self):
        return f"<DeliveryPerson(DeliveryPersonID={self.DeliveryPersonID}, Name='{self.Name}')>"
