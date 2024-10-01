from sqlalchemy import Column, Integer, String, Text, Boolean, Date, DECIMAL
from database import Base

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

