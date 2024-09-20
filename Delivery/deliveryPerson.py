from sqlalchemy import Column, Integer, String, Boolean
from db import Base, session

class DeliveryPerson(Base):
    __tablename__ = 'DeliveryPerson'

    DeliveryPersonID = Column(Integer, primary_key=True, autoincrement=True)
    Name = Column(String(255), nullable=False)
    AssignedPostalCode = Column(String(255), nullable=False)
    IsAvailable = Column(Boolean, nullable=False)

    def __repr__(self):
        return (f"<DeliveryPerson(DeliveryPersonID={self.DeliveryPersonID}, Name='{self.Name}', "
                f"AssignedPostalCode='{self.AssignedPostalCode}', IsAvailable={self.IsAvailable})>")

# Function to add a delivery person
def add_delivery_person(name, assigned_postal_code, is_available):
    new_delivery_person = DeliveryPerson(
        Name=name,
        AssignedPostalCode=assigned_postal_code,
        IsAvailable=is_available
    )
    session.add(new_delivery_person)
    session.commit()
    print(f"Delivery Person '{name}' added to the database.")
