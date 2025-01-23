from database import SessionLocal
import models
import json
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Customer
from database import SQLALCHEMY_DATABASE_URL

def calculate_loan_eligibility_metrics(customer_data, bureau_data):
    # Use the exact same credit score from bureau_data
    eligibility_score = bureau_data.credit_score
    
    # Determine score range
    if eligibility_score >= 750:
        score_range = "Excellent"
    elif eligibility_score >= 700:
        score_range = "Good"
    elif eligibility_score >= 650:
        score_range = "Fair"
    else:
        score_range = "Poor"
    
    # Calculate DTI ratio (monthly obligations / monthly income)
    monthly_income = customer_data["profile"]["salary"] / 12
    monthly_obligations = (
        bureau_data.loan_details["home_loan"]["monthly_emi"] +
        bureau_data.loan_details["car_loan"]["monthly_emi"]
    )
    dti_ratio = (monthly_obligations / monthly_income) * 100
    
    # Determine DTI status
    if dti_ratio <= 30:
        dti_status = "Good Standing"
    elif dti_ratio <= 40:
        dti_status = "Warning"
    else:
        dti_status = "Critical"
    
    # Current EMI load is the sum of all EMIs
    current_emi_load = monthly_obligations
    
    # Determine EMI status based on 50% of income threshold
    emi_threshold = monthly_income * 0.5
    if current_emi_load <= emi_threshold * 0.7:
        emi_status = "Below Threshold"
    elif current_emi_load <= emi_threshold * 0.9:
        emi_status = "Near Threshold"
    else:
        emi_status = "Above Threshold"
    
    return {
        "eligibility_score": int(eligibility_score),
        "score_range": score_range,
        "debt_to_income_ratio": float(dti_ratio),
        "dti_status": dti_status,
        "current_emi_load": float(current_emi_load),
        "emi_status": emi_status
    }

def create_sample_data():
    db = SessionLocal()

    # Sample customers data
    customers_data = [
        {
            "name": "Rahul Sharma",
            "email": "rahul.sharma@gmail.com",
            "profile": {
                "salary": 1500000,
                "occupation": "Software Engineer",
                "company": "Tech Solutions Ltd"
            }
        },
        {
            "name": "Priya Patel",
            "email": "priya.patel@yahoo.com",
            "profile": {
                "salary": 2500000,
                "occupation": "Senior Manager",
                "company": "Global Finance Corp"
            }
        },
        {
            "name": "Amit Kumar",
            "email": "amit.kumar@outlook.com",
            "profile": {
                "salary": 800000,
                "occupation": "Business Owner",
                "company": "Kumar Enterprises"
            }
        },
        {
            "name": "Sneha Reddy",
            "email": "sneha.reddy@hotmail.com",
            "profile": {
                "salary": 1800000,
                "occupation": "Data Scientist",
                "company": "Analytics India"
            }
        },
        {
            "name": "Vikram Singh",
            "email": "vikram.singh@gmail.com",
            "profile": {
                "salary": 3500000,
                "occupation": "Investment Banker",
                "company": "Capital Markets Ltd"
            }
        }
    ]

    # Create customers and their data
    for customer_data in customers_data:
        # Create customer
        customer = models.Customer(
            name=customer_data["name"],
            email=customer_data["email"]
        )
        db.add(customer)
        db.commit()
        db.refresh(customer)

        # Create AA Data
        aa_data = models.AAData(
            customer_id=customer.id,
            account_summary={
                "savings_account": {
                    "balance": customer_data["profile"]["salary"] * 0.4,  # 4 months salary as savings
                    "bank": "HDFC Bank",
                    "account_type": "Savings",
                    "monthly_average": customer_data["profile"]["salary"] * 0.3
                },
                "fixed_deposits": [
                    {
                        "amount": customer_data["profile"]["salary"] * 0.8,
                        "interest_rate": 7.5,
                        "maturity_date": "2024-12-31"
                    }
                ]
            },
            spending_patterns={
                "categories": {
                    "groceries": customer_data["profile"]["salary"] * 0.08 / 12,
                    "utilities": customer_data["profile"]["salary"] * 0.05 / 12,
                    "entertainment": customer_data["profile"]["salary"] * 0.06 / 12,
                    "dining": customer_data["profile"]["salary"] * 0.07 / 12,
                    "transportation": customer_data["profile"]["salary"] * 0.04 / 12
                },
                "monthly_average_spend": customer_data["profile"]["salary"] * 0.3 / 12,
                "highest_spend_category": "groceries"
            },
            assets={
                "total_value": customer_data["profile"]["salary"] * 3,
                "breakdown": {
                    "real_estate": customer_data["profile"]["salary"] * 1.5,
                    "vehicles": customer_data["profile"]["salary"] * 0.5,
                    "investments": customer_data["profile"]["salary"] * 1.0
                }
            }
        )

        # Calculate credit score based on salary and profile
        base_credit_score = 750
        salary_factor = min(50, (customer_data["profile"]["salary"] // 500000) * 5)
        credit_score = min(850, base_credit_score + salary_factor)

        # Create Bureau Data with calculated credit score
        bureau_data = models.BureauData(
            customer_id=customer.id,
            credit_score=credit_score,  # Use calculated credit score
            loan_details={
                "home_loan": {
                    "principal": customer_data["profile"]["salary"] * 4,
                    "remaining": customer_data["profile"]["salary"] * 3,
                    "interest_rate": 8.5,
                    "tenure_months": 180,
                    "monthly_emi": (customer_data["profile"]["salary"] * 4 * 0.08) / 12
                },
                "car_loan": {
                    "principal": customer_data["profile"]["salary"] * 0.8,
                    "remaining": customer_data["profile"]["salary"] * 0.6,
                    "interest_rate": 9.5,
                    "tenure_months": 60,
                    "monthly_emi": (customer_data["profile"]["salary"] * 0.8 * 0.095) / 12
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

        # Create loan eligibility metrics using the same credit score
        metrics = calculate_loan_eligibility_metrics(customer_data, bureau_data)
        loan_eligibility = models.LoanEligibilityMetrics(
            customer_id=customer.id,
            **metrics
        )
        db.add(loan_eligibility)

        # Create ITR Data
        itr_data = models.ITRData(
            customer_id=customer.id,
            taxable_income=customer_data["profile"]["salary"],
            tax_returns={
                "fy_2022_23": {
                    "gross_income": customer_data["profile"]["salary"] * 1.2,
                    "taxable_income": customer_data["profile"]["salary"],
                    "tax_paid": customer_data["profile"]["salary"] * 0.2
                }
            },
            deductions={
                "80C": 150000,
                "80D": 25000,
                "home_loan_interest": min(200000, customer_data["profile"]["salary"] * 0.15),
                "standard_deduction": 50000
            }
        )

        # Create sample transactions
        transactions = [
            models.Transaction(
                customer_id=customer.id,
                amount=bureau_data.loan_details["home_loan"]["monthly_emi"],
                description="Home Loan EMI Payment"
            ),
            models.Transaction(
                customer_id=customer.id,
                amount=bureau_data.loan_details["car_loan"]["monthly_emi"],
                description="Car Loan EMI Payment"
            ),
            models.Transaction(
                customer_id=customer.id,
                amount=customer_data["profile"]["salary"] / 12,
                description="Salary Credit"
            ),
            models.Transaction(
                customer_id=customer.id,
                amount=-aa_data.spending_patterns["categories"]["groceries"],
                description="Grocery Shopping"
            ),
            models.Transaction(
                customer_id=customer.id,
                amount=-aa_data.spending_patterns["categories"]["utilities"],
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

# Create database engine and session
engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Sample demographic data
customer_demographics = [
    {
        "email": "rahul.sharma@gmail.com",
        "age": 32,
        "occupation": "Software Engineer",
        "interests": ["technology", "travel", "dining"],
        "lifestyle_preferences": {
            "dining_frequency": "frequent",
            "travel_frequency": "moderate",
            "shopping_preference": "online",
            "entertainment": "movies_and_events",
            "fitness": "gym_enthusiast"
        }
    },
    {
        "email": "priya.patel@yahoo.com",
        "age": 28,
        "occupation": "Marketing Manager",
        "interests": ["shopping", "dining", "fashion"],
        "lifestyle_preferences": {
            "dining_frequency": "moderate",
            "travel_frequency": "occasional",
            "shopping_preference": "luxury_retail",
            "entertainment": "fine_dining",
            "fitness": "yoga"
        }
    },
    {
        "email": "amit.kumar@outlook.com",
        "age": 45,
        "occupation": "Business Owner",
        "interests": ["business", "golf", "luxury_travel"],
        "lifestyle_preferences": {
            "dining_frequency": "frequent",
            "travel_frequency": "frequent",
            "shopping_preference": "premium_brands",
            "entertainment": "golf_and_clubs",
            "fitness": "personal_trainer"
        }
    },
    {
        "email": "sneha.reddy@hotmail.com",
        "age": 35,
        "occupation": "Doctor",
        "interests": ["health", "travel", "books"],
        "lifestyle_preferences": {
            "dining_frequency": "moderate",
            "travel_frequency": "frequent",
            "shopping_preference": "quality_focused",
            "entertainment": "cultural_events",
            "fitness": "running"
        }
    },
    {
        "email": "vikram.singh@gmail.com",
        "age": 29,
        "occupation": "Financial Analyst",
        "interests": ["finance", "fitness", "technology"],
        "lifestyle_preferences": {
            "dining_frequency": "moderate",
            "travel_frequency": "occasional",
            "shopping_preference": "value_focused",
            "entertainment": "sports",
            "fitness": "crossfit"
        }
    }
]

def update_customer_demographics():
    """Update existing customers with demographic information"""
    db = SessionLocal()
    try:
        print("Updating customer demographics...")
        
        for demo_data in customer_demographics:
            # Find existing customer by email
            customer = db.query(Customer).filter(Customer.email == demo_data["email"]).first()
            if customer:
                print(f"Updating demographics for {demo_data['email']}")
                customer.age = demo_data["age"]
                customer.occupation = demo_data["occupation"]
                customer.interests = demo_data["interests"]
                customer.lifestyle_preferences = demo_data["lifestyle_preferences"]
            else:
                print(f"Customer not found: {demo_data['email']}")
        
        db.commit()
        print("Demographics update completed successfully!")
        
    except Exception as e:
        print(f"Error updating demographics: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_data()
    update_customer_demographics() 