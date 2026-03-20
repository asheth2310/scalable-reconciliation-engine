import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from app.database import Base

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    vendor_name = Column(String, index=True)
    amount = Column(Float)
    reference_number = Column(String, unique=True, index=True)
    status = Column(String, default="PENDING")  # PENDING, RECONCILED, DISCREPANCY
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class ReconciliationLog(Base):
    __tablename__ = "reconciliation_logs"

    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, index=True)
    action_taken = Column(String)
    system_confidence = Column(Float)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
