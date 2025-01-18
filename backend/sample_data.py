from database import SessionLocal
import models
import json

def create_sample_data():
    db = SessionLocal()

    # Create a sample customer
    customer = models.Customer(
        name="John Smith",
        email="john.smith@example.com"
    )
    db.add(customer)
    db.commit()
    db.refresh(customer)

    # Sample AA (Account Aggregator) Data
    aa_data = models.AAData(
        customer_id=customer.id,
        account_summary={
            "savings_account": {
                "balance": 150000,
                "bank": "HDFC Bank",
                "account_type": "Savings",
                "monthly_average": 125000
            },
            "fixed_deposits": [
                {
                    "amount": 500000,
                    "interest_rate": 7.5,
                    "maturity_date": "2024-12-31"
                }
            ]
        },
        spending_patterns={
            "categories": {
                "groceries": 15000,
                "utilities": 8000,
                "entertainment": 5000,
                "dining": 10000,
                "transportation": 6000
            },
            "monthly_average_spend": 44000,
            "highest_spend_category": "groceries"
        },
        assets={
            "total_value": 2500000,
            "breakdown": {
                "real_estate": 1500000,
                "vehicles": 500000,
                "investments": 500000
            }
        }
    )

    # Sample Bureau Data
    bureau_data = models.BureauData(
        customer_id=customer.id,
        credit_score=750,
        loan_details={
            "home_loan": {
                "principal": 3000000,
                "remaining": 2500000,
                "interest_rate": 8.5,
                "tenure_months": 180,
                "monthly_emi": 35000
            },
            "car_loan": {
                "principal": 800000,
                "remaining": 600000,
                "interest_rate": 9.5,
                "tenure_months": 60,
                "monthly_emi": 15000
            }
        },
        repayment_history={
            "total_loans": 3,
            "active_loans": 2,
            "on_time_payments": "95%",
            "last_12_months": {
                "payments_made": 24,
                "late_payments": 1
            }
        }
    )

    # Sample ITR Data
    itr_data = models.ITRData(
        customer_id=customer.id,
        taxable_income=1200000,
        tax_returns={
            "fy_2022_23": {
                "gross_income": 1500000,
                "taxable_income": 1200000,
                "tax_paid": 125000
            }
        },
        deductions={
            "80C": 150000,
            "80D": 25000,
            "home_loan_interest": 200000,
            "standard_deduction": 50000
        }
    )

    # Sample Transactions
    transactions = [
        models.Transaction(
            customer_id=customer.id,
            amount=35000,
            description="Home Loan EMI Payment"
        ),
        models.Transaction(
            customer_id=customer.id,
            amount=15000,
            description="Car Loan EMI Payment"
        ),
        models.Transaction(
            customer_id=customer.id,
            amount=50000,
            description="Salary Credit"
        ),
        models.Transaction(
            customer_id=customer.id,
            amount=-15000,
            description="Grocery Shopping"
        ),
        models.Transaction(
            customer_id=customer.id,
            amount=-8000,
            description="Utility Bills"
        )
    ]

    db.add(aa_data)
    db.add(bureau_data)
    db.add(itr_data)
    for transaction in transactions:
        db.add(transaction)

    db.commit()
    print("Sample data created successfully!")
    db.close()

if __name__ == "__main__":
    create_sample_data() 