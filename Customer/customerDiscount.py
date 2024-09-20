from sqlalchemy import Column, Integer, ForeignKey
from db import Base, session

class CustomerDiscount(Base):
    __tablename__ = 'CustomerDiscount'

    CustomerID = Column(Integer, ForeignKey('Customer.CustomerID'), primary_key=True)
    DiscountCodeID = Column(Integer, ForeignKey('DiscountCode.DiscountCodeID'), primary_key=True)

    def __repr__(self):
        return f"<CustomerDiscount(CustomerID={self.CustomerID}, DiscountCodeID={self.DiscountCodeID})>"

# Function to add a customer discount
def add_customer_discount(customer_id, discount_code_id):
    new_customer_discount = CustomerDiscount(
        CustomerID=customer_id,
        DiscountCodeID=discount_code_id
    )
    session.add(new_customer_discount)
    session.commit()
    print(f"CustomerDiscount for CustomerID '{customer_id}' and DiscountCodeID '{discount_code_id}' added to the database.")
