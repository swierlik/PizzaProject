import datetime

from sqlalchemy import Column, Integer, String, Text, Boolean, Date, DECIMAL
from db import Base, session

class DiscountCode(Base):
    __tablename__ = 'DiscountCode'

    DiscountCodeID = Column(Integer, primary_key=True, autoincrement=True)
    Code = Column(String(255), nullable=False)
    Description = Column(Text, nullable=True)
    IsRedeemed = Column(Boolean, nullable=False, default=False)
    ExpiryDate = Column(Date, nullable=False)
    DiscountPercentage = Column(DECIMAL(10, 2), nullable=False)

    def __repr__(self):
        return (f"<DiscountCode(DiscountCodeID={self.DiscountCodeID}, Code='{self.Code}', "
                f"Description='{self.Description}', IsRedeemed={self.IsRedeemed}, ExpiryDate={self.ExpiryDate})>")

# Function to add a discount code
def add_discount_code(code, description, expiry_date, discount_percentage):
    new_discount_code = DiscountCode(
        Code=code,
        Description=description,
        ExpiryDate=expiry_date,
        DiscountPercentage=discount_percentage
    )
    session.add(new_discount_code)
    session.commit()
    print(f"Discount Code '{code}' added to the database.")

def use_code(code):
    discount_code = session.query(DiscountCode).filter(DiscountCode.Code == code).first()
    if discount_code is None:
        print("Discount code not found.")
        return False
    if discount_code.IsRedeemed:
        print("Discount code has already been redeemed.")
        return False
    if discount_code.ExpiryDate < datetime.now().date():
        print("Discount code has expired.")
        return False
    discount_code.IsRedeemed = True
    session.commit()
    print(f"Discount code '{code}' has been redeemed.")
    return True

def get_discount_by_code(code, price):
    if use_code(code):
        discount_code = session.query(DiscountCode).filter(DiscountCode.Code == code).first()
        return price*discount_code.DiscountPercentage
