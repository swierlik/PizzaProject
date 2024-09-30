from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from db import Base, session
from Delivery.deliveryPerson import set_availability

class Delivery(Base):
    __tablename__ = 'Delivery'

    DeliveryID = Column(Integer, primary_key=True, autoincrement=True)
    OrderID = Column(Integer, nullable=False)
    DeliveryPersonID = Column(Integer, ForeignKey('DeliveryPerson.DeliveryPersonID'), nullable=False)
    DeliveryStatus = Column(String(255), nullable=False)
    DeliveryTime = Column(TIMESTAMP, nullable=False)

    def __repr__(self):
        return (f"<Delivery(DeliveryID={self.DeliveryID}, OrderID={self.OrderID}, "
                f"DeliveryPersonID={self.DeliveryPersonID}, DeliveryStatus='{self.DeliveryStatus}', "
                f"DeliveryTime={self.DeliveryTime})>")

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
    set_availability(delivery_person_id, False)

    session.commit()
    print(f"Delivery for OrderID '{order_id}' added to the database.")

def update_delivery_status(deliveryID, status):
    delivery = session.query(Delivery).filter(Delivery.DeliveryID == deliveryID).first()
    delivery.DeliveryStatus = status
    session.commit()
    print(f"Delivery Status for DeliveryID '{deliveryID}' updated to '{status}'.")

def get_delivery_person_id(deliveryID):
    delivery = session.query(Delivery).filter(Delivery.DeliveryID == deliveryID).first()
    return delivery.DeliveryPersonID

def get_delivery_status(deliveryID):
    delivery = session.query(Delivery).filter(Delivery.DeliveryID == deliveryID).first()
    return delivery.DeliveryStatus

def get_delivery_time(deliveryID):
    delivery = session.query(Delivery).filter(Delivery.DeliveryID == deliveryID).first()
    return delivery.DeliveryTime

def update_status(delivertyID):
    delivery = session.query(Delivery).filter(Delivery.DeliveryID == delivertyID).first()
    
