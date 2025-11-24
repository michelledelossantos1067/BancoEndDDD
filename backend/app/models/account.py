from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.database.config import Base

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    account_number = Column(String, unique=True, index=True, nullable=False)
    holder_name = Column(String, nullable=False)
    holder_id = Column(String, unique=True, nullable=False)
    account_type = Column(String, nullable=False)
    balance = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.timezone.utc)
    updated_at = Column(DateTime, default=datetime.time, onupdate=datetime.timezone.utc)

    def to_dict(self):
        return {
            "id": self.id,
            "account_number": self.account_number,
            "holder_name": self.holder_name,
            "holder_id": self.holder_id,
            "account_type": self.account_type,
            "balance": self.balance,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }