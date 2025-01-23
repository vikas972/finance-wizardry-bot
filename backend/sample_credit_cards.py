from database import SessionLocal
import models
from rag_utils import RAGPipeline

def create_sample_credit_cards():
    db = SessionLocal()
    rag_pipeline = RAGPipeline()

    credit_cards_data = [
        {
            "bank_name": "HDFC Bank",
            "card_name": "Regalia First",
            "card_type": "lifestyle",
            "annual_fee": 1000,
            "renewal_fee": 1000,
            "interest_rate": 42.0,
            "min_credit_score": 750,
            "min_income": 600000,
            "welcome_benefits": {
                "reward_points": 2500,
                "milestone_benefits": "10,000 reward points on spending ₹1,50,000 in 90 days"
            },
            "reward_points": {
                "regular_spend": 4,
                "accelerated_categories": {
                    "dining": 8,
                    "shopping": 8
                },
                "point_value": 0.30  # Value per point in INR
            },
            "cashback_details": None,
            "travel_benefits": {
                "lounge_access": {
                    "domestic": 12,
                    "international": 6
                },
                "insurance": {
                    "travel": "Up to ₹1 Crore",
                    "lost_card": "₹50,000"
                }
            },
            "lifestyle_benefits": {
                "dining": "1+1 at fine dining restaurants",
                "movies": "1+1 on BookMyShow",
                "shopping": "Exclusive discounts on premium brands"
            },
            "card_features": {
                "contactless": True,
                "emv_chip": True,
                "fuel_surcharge_waiver": "1%",
                "emi_options": True
            },
            "eligibility_criteria": {
                "salaried": True,
                "self_employed": True,
                "min_age": 21,
                "max_age": 60,
                "documents": ["PAN", "Aadhaar", "Income Proof"]
            },
            "terms_conditions": "Standard terms and conditions apply. Interest rates and fees subject to change."
        },
        {
            "bank_name": "ICICI Bank",
            "card_name": "Amazon Pay Credit Card",
            "card_type": "cashback",
            "annual_fee": 500,
            "renewal_fee": 500,
            "interest_rate": 41.0,
            "min_credit_score": 700,
            "min_income": 300000,
            "welcome_benefits": {
                "amazon_voucher": 1000,
                "joining_bonus": "₹500 Amazon Pay balance"
            },
            "reward_points": None,
            "cashback_details": {
                "amazon": 5.0,
                "amazon_prime": 5.0,
                "utilities": 2.0,
                "other": 1.0,
                "max_monthly_cashback": 2500
            },
            "travel_benefits": {
                "lounge_access": {
                    "domestic": 4,
                    "international": 0
                },
                "insurance": {
                    "travel": "Up to ₹50 Lakhs",
                    "lost_card": "₹25,000"
                }
            },
            "lifestyle_benefits": {
                "amazon_prime": "Free for first year",
                "shopping": "Extra discounts on Amazon.in"
            },
            "card_features": {
                "contactless": True,
                "emv_chip": True,
                "fuel_surcharge_waiver": "1%",
                "emi_options": True
            },
            "eligibility_criteria": {
                "salaried": True,
                "self_employed": True,
                "min_age": 18,
                "max_age": 65,
                "documents": ["PAN", "Aadhaar", "Income Proof"]
            },
            "terms_conditions": "Cashback will be credited as Amazon Pay balance. Terms and conditions apply."
        },
        {
            "bank_name": "SBI Card",
            "card_name": "ELITE",
            "card_type": "travel",
            "annual_fee": 4999,
            "renewal_fee": 4999,
            "interest_rate": 43.0,
            "min_credit_score": 750,
            "min_income": 1800000,
            "welcome_benefits": {
                "reward_points": 5000,
                "milestone_benefits": "20,000 bonus points on spending ₹2,00,000 in 60 days"
            },
            "reward_points": {
                "regular_spend": 5,
                "accelerated_categories": {
                    "travel": 10,
                    "dining": 8
                },
                "point_value": 0.25  # Value per point in INR
            },
            "cashback_details": None,
            "travel_benefits": {
                "lounge_access": {
                    "domestic": "Unlimited",
                    "international": 6
                },
                "insurance": {
                    "travel": "Up to ₹2 Crore",
                    "lost_card": "₹1,00,000",
                    "purchase_protection": "₹2,00,000"
                }
            },
            "lifestyle_benefits": {
                "dining": "Up to 15% discount at partner restaurants",
                "hotels": "Special rates at luxury hotels",
                "golf": "Complimentary green fee at select golf courses"
            },
            "card_features": {
                "contactless": True,
                "emv_chip": True,
                "fuel_surcharge_waiver": "1%",
                "emi_options": True,
                "concierge": True
            },
            "eligibility_criteria": {
                "salaried": True,
                "self_employed": True,
                "min_age": 21,
                "max_age": 65,
                "documents": ["PAN", "Aadhaar", "Income Proof", "Latest ITR"]
            },
            "terms_conditions": "Premium travel credit card with exclusive benefits. Terms and conditions apply."
        }
    ]

    for card_data in credit_cards_data:
        # Create text for embedding
        card_text = f"""
        {card_data['bank_name']} {card_data['card_name']}
        Type: {card_data['card_type']}
        Annual Fee: ₹{card_data['annual_fee']}
        Minimum Income: ₹{card_data['min_income']}
        Key Benefits:
        - Welcome Benefits: {str(card_data['welcome_benefits'])}
        - Reward Points: {str(card_data['reward_points'])}
        - Cashback: {str(card_data['cashback_details'])}
        - Travel Benefits: {str(card_data['travel_benefits'])}
        - Lifestyle Benefits: {str(card_data['lifestyle_benefits'])}
        """
        
        # Generate embedding
        vector_embedding = rag_pipeline.generate_embedding(card_text)
        
        # Create credit card entry
        credit_card = models.CreditCard(
            **card_data,
            vector_embedding=vector_embedding
        )
        db.add(credit_card)

    # Sample credit card preferences for existing customers
    customers = db.query(models.Customer).all()
    for customer in customers:
        # Create preferences based on customer profile
        monthly_income = customer.itr_data[0].taxable_income / 12 if customer.itr_data else 50000
        spending_patterns = customer.aa_data[0].spending_patterns if customer.aa_data else {}
        
        preferences = {
            "customer_id": customer.id,
            "preferred_categories": ["travel", "dining", "shopping"],
            "max_annual_fee": monthly_income * 0.01,  # 1% of monthly income
            "preferred_reward_type": "points" if monthly_income > 100000 else "cashback",
            "lifestyle_preferences": ["movies", "dining", "shopping"],
            "travel_frequency": "frequently" if monthly_income > 150000 else "occasionally",
            "current_cards": {
                "count": 1,
                "banks": ["HDFC Bank"]
            },
            "monthly_spending": spending_patterns.get("categories", {})
        }
        
        credit_card_pref = models.CustomerCreditCardPreference(**preferences)
        db.add(credit_card_pref)

    db.commit()
    print("Sample credit card data created successfully!")
    db.close()

if __name__ == "__main__":
    create_sample_credit_cards() 