from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Text, Boolean, ARRAY
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
    loan_eligibility_metrics = relationship("LoanEligibilityMetrics", back_populates="customer", uselist=False)
    credit_card_preferences = relationship("CustomerCreditCardPreference", back_populates="customer", uselist=False)

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

class LoanEligibilityMetrics(Base):
    __tablename__ = "loan_eligibility_metrics"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    eligibility_score = Column(Integer)
    score_range = Column(String)  # e.g., "Excellent", "Good", "Fair", "Poor"
    debt_to_income_ratio = Column(Float)
    dti_status = Column(String)  # e.g., "Good Standing", "Warning", "Critical"
    current_emi_load = Column(Float)
    emi_status = Column(String)  # e.g., "Below Threshold", "Near Threshold", "Above Threshold"

    customer = relationship("Customer", back_populates="loan_eligibility_metrics")

class CreditCard(Base):
    __tablename__ = "credit_cards"

    id = Column(Integer, primary_key=True, index=True)
    bank_name = Column(String, index=True)
    card_name = Column(String, index=True)
    card_type = Column(String)  # travel, cashback, lifestyle, etc.
    annual_fee = Column(Float)
    renewal_fee = Column(Float)
    interest_rate = Column(Float)  # APR
    min_credit_score = Column(Integer)
    min_income = Column(Float)
    welcome_benefits = Column(JSON)
    reward_points = Column(JSON)  # Structure for reward point system
    cashback_details = Column(JSON)  # Structure for cashback rules
    travel_benefits = Column(JSON)  # Lounge access, travel insurance, etc.
    lifestyle_benefits = Column(JSON)  # Shopping, dining, entertainment
    card_features = Column(JSON)  # EMI options, fuel surcharge waiver, etc.
    eligibility_criteria = Column(JSON)
    terms_conditions = Column(Text)
    vector_embedding = Column(Text)  # For semantic search
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class CustomerCreditCardPreference(Base):
    __tablename__ = "customer_credit_card_preferences"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    preferred_categories = Column(ARRAY(String))  # ['travel', 'dining', 'shopping']
    max_annual_fee = Column(Float)
    preferred_reward_type = Column(String)  # points, cashback, miles
    lifestyle_preferences = Column(ARRAY(String))  # ['movies', 'dining', 'shopping']
    travel_frequency = Column(String)  # rarely, occasionally, frequently
    current_cards = Column(JSON)  # List of current credit cards
    monthly_spending = Column(JSON)  # Spending patterns by category
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    customer = relationship("Customer", back_populates="credit_card_preferences") 