# Customers/CustomerDiscount.py
from sqlalchemy import Column, Integer, ForeignKey
from database import Base

class CustomerDiscount(Base):
    __tablename__ = 'CustomerDiscount'

    # Correct the foreign key reference to match the actual table name
    CustomerID = Column(Integer, ForeignKey('customers.CustomerID'), primary_key=True)
    DiscountCodeID = Column(Integer, ForeignKey('DiscountCode.DiscountCodeID'), primary_key=True)

    def __repr__(self):
        return f"<CustomerDiscount(CustomerID={self.CustomerID}, DiscountCodeID={self.DiscountCodeID})>"
