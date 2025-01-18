from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional, Dict, Any

class TransactionBase(BaseModel):
    amount: float
    description: str

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    customer_id: int
    transaction_date: datetime

    class Config:
        from_attributes = True

class AADataBase(BaseModel):
    account_summary: Dict[str, Any]
    spending_patterns: Dict[str, Any]
    assets: Dict[str, Any]

class AADataCreate(AADataBase):
    pass

class AAData(AADataBase):
    id: int
    customer_id: int
    created_at: datetime
    vector_embedding: Optional[str] = None

    class Config:
        from_attributes = True

class BureauDataBase(BaseModel):
    loan_details: Dict[str, Any]
    credit_score: int
    repayment_history: Dict[str, Any]

class BureauDataCreate(BureauDataBase):
    pass

class BureauData(BureauDataBase):
    id: int
    customer_id: int
    created_at: datetime
    vector_embedding: Optional[str] = None

    class Config:
        from_attributes = True

class ITRDataBase(BaseModel):
    tax_returns: Dict[str, Any]
    taxable_income: float
    deductions: Dict[str, Any]

class ITRDataCreate(ITRDataBase):
    pass

class ITRData(ITRDataBase):
    id: int
    customer_id: int
    created_at: datetime
    vector_embedding: Optional[str] = None

    class Config:
        from_attributes = True

class CustomerBase(BaseModel):
    name: str
    email: str

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    id: int
    created_at: datetime
    transactions: List[Transaction] = []
    aa_data: List[AAData] = []
    bureau_data: List[BureauData] = []
    itr_data: List[ITRData] = []

    class Config:
        from_attributes = True 