
from db import session
from models.Delivery import Delivery
from models.DeliveryPerson import DeliveryPerson

# Function to add a delivery
def add_delivery(order_id, delivery_person_id, delivery_status, delivery_time):
    new_delivery = Delivery(
        OrderID=order_id,
        DeliveryPersonID=delivery_person_id,
        DeliveryStatus=delivery_status,
        DeliveryTime=delivery_time
    )
    session.add(new_delivery)

    # Update delivery person availability
    set_availability(session,delivery_person_id, False)

    session.commit()
    print(f"Delivery for OrderID '{order_id}' added to the database.")

def update_delivery_status(deliveryID, status):
    delivery = session.query(Delivery).filter(Delivery.DeliveryID == deliveryID).first()
    delivery.DeliveryStatus = status
    session.commit()
    print(f"Delivery Status for DeliveryID '{deliveryID}' updated to '{status}'.")

def set_availability(session, delivery_person_id, availability):
    delivery_person = session.query(DeliveryPerson).filter(DeliveryPerson.DeliveryPersonID == delivery_person_id).first()
    delivery_person.Available = availability
    session.commit()

def get_delivery_person_id(deliveryID):
    delivery = session.query(Delivery).filter(Delivery.DeliveryID == deliveryID).first()
    return delivery.DeliveryPersonID

def get_delivery_status(deliveryID):
    delivery = session.query(Delivery).filter(Delivery.DeliveryID == deliveryID).first()
    return delivery.DeliveryStatus

def get_delivery_time(deliveryID):
    delivery = session.query(Delivery).filter(Delivery.DeliveryID == deliveryID).first()
    return delivery.DeliveryTime

def add_delivery_person(name, postal_code):
    new_delivery_person = DeliveryPerson(
        Name=name,
        PostalCode=postal_code,
        IsAvailable=True
    )
    session.add(new_delivery_person)
    session.commit()
    print(f"Delivery Person '{name}' added to the database.")

def find_available_delivery_person(postal_code):
    delivery_person = session.query(DeliveryPerson).filter(DeliveryPerson.PostalCode == postal_code, DeliveryPerson.IsAvailable == True).first()
    if delivery_person is None:
        print("No available delivery person found.")
        return None
    return delivery_person.DeliveryPersonID

def get_driver_by_id(driver_id):
    return session.query(DeliveryPerson).filter(DeliveryPerson.DeliveryPersonID == driver_id).first()
    
