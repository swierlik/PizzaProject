from sqlalchemy import Column, Integer, String, Text, Boolean, Date
from db import Base, session

class DiscountCode(Base):
    __tablename__ = 'DiscountCode'

    DiscountCodeID = Column(Integer, primary_key=True, autoincrement=True)
    Code = Column(String(255), nullable=False)
    Description = Column(Text, nullable=True)
    IsRedeemed = Column(Boolean, nullable=False, default=False)
    ExpiryDate = Column(Date, nullable=False)

    def __repr__(self):
        return (f"<DiscountCode(DiscountCodeID={self.DiscountCodeID}, Code='{self.Code}', "
                f"Description='{self.Description}', IsRedeemed={self.IsRedeemed}, ExpiryDate={self.ExpiryDate})>")

# Function to add a discount code
def add_discount_code(code, description, is_redeemed, expiry_date):
    new_discount_code = DiscountCode(
        Code=code,
        Description=description,
        IsRedeemed=is_redeemed,
        ExpiryDate=expiry_date
    )
    session.add(new_discount_code)
    session.commit()
    print(f"Discount Code '{code}' added to the database.")
