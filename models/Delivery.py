from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from db import Base


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

