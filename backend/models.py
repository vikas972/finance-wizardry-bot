from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    transactions = relationship("Transaction", back_populates="customer")
    aa_data = relationship("AAData", back_populates="customer")
    bureau_data = relationship("BureauData", back_populates="customer")
    itr_data = relationship("ITRData", back_populates="customer")

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    amount = Column(Float)
    description = Column(String)
    transaction_date = Column(DateTime(timezone=True), server_default=func.now())
    customer = relationship("Customer", back_populates="transactions")

class AAData(Base):
    __tablename__ = "aa_data"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    account_summary = Column(JSON)
    spending_patterns = Column(JSON)
    assets = Column(JSON)
    vector_embedding = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    customer = relationship("Customer", back_populates="aa_data")

class BureauData(Base):
    __tablename__ = "bureau_data"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    loan_details = Column(JSON)
    credit_score = Column(Integer)
    repayment_history = Column(JSON)
    vector_embedding = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    customer = relationship("Customer", back_populates="bureau_data")

class ITRData(Base):
    __tablename__ = "itr_data"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    tax_returns = Column(JSON)
    taxable_income = Column(Float)
    deductions = Column(JSON)
    vector_embedding = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    customer = relationship("Customer", back_populates="itr_data") 