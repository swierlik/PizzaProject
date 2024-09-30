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
def add_delivery_person(name, assigned_postal_code):
    new_delivery_person = DeliveryPerson(
        Name=name,
        AssignedPostalCode=assigned_postal_code,
        IsAvailable=True
    )
    session.add(new_delivery_person)
    session.commit()
    print(f"Delivery Person '{name}' added to the database.")

def check_availability(deliveryPersonID):
    deliveryPerson = session.query(DeliveryPerson).filter(DeliveryPerson.DeliveryPersonID == deliveryPersonID).first()
    return deliveryPerson.IsAvailable

def set_availability(deliveryPersonID, availability):
    deliveryPerson = session.query(DeliveryPerson).filter(DeliveryPerson.DeliveryPersonID == deliveryPersonID).first()
    deliveryPerson.IsAvailable = availability
    session.commit()
    print(f"Delivery Person '{deliveryPerson.Name}' availability set to {availability}.")

def find_available_delivery_person(postal_code):
    delivery_person = session.query(DeliveryPerson).filter(DeliveryPerson.AssignedPostalCode == postal_code).filter(DeliveryPerson.IsAvailable == True).first()
    if delivery_person is None:
        print("No available delivery person found.")
        return None
    delivery_person.IsAvailable = False
    return delivery_person.DeliveryPersonID
