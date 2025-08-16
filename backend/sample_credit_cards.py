from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, CreditCard, CreditCardUpdate
from database import SQLALCHEMY_DATABASE_URL
import json

# Create database engine and session
engine = create_engine(SQLALCHEMY_DATABASE_URL)
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def convert_to_json_string(data):
    """Convert dictionary to JSON string"""
    return json.dumps(data, ensure_ascii=False)

# Sample credit card data
credit_cards = [
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
            "reward_points": 5000,
            "milestone_bonus": "2X reward points on reaching ₹1,50,000 spend"
        },
        "reward_points": {
            "regular_spend": 4,
            "premium_spend": 8,
            "max_points": 10000
        },
        "cashback_details": {
            "regular": "1% on all spends",
            "special": "5% on weekend dining"
        },
        "travel_benefits": {
            "lounge_access": "8 complimentary domestic lounge visits per year",
            "insurance": "Travel insurance up to ₹50 lakhs"
        },
        "lifestyle_benefits": {
            "dining": "1+1 at partner restaurants",
            "movies": "Buy 1 Get 1 on BookMyShow"
        }
    },
    {
        "bank_name": "ICICI Bank",
        "card_name": "Amazon Pay Signature",
        "card_type": "shopping",
        "annual_fee": 3000,
        "renewal_fee": 3000,
        "interest_rate": 41.0,
        "min_credit_score": 700,
        "min_income": 720000,
        "welcome_benefits": {
            "amazon_voucher": "₹3000 Amazon Pay gift card",
            "reward_points": 3000
        },
        "reward_points": {
            "amazon_spend": 5,
            "regular_spend": 2,
            "max_points": "Unlimited"
        },
        "cashback_details": {
            "amazon": "5% on Amazon.in",
            "regular": "1% on all other spends"
        },
        "travel_benefits": {
            "lounge_access": "4 domestic airport lounge visits per quarter",
            "fuel_surcharge": "1% fuel surcharge waiver"
        },
        "lifestyle_benefits": {
            "dining": "2X rewards on dining",
            "entertainment": "2X rewards on entertainment"
        }
    },
    {
        "bank_name": "SBI Card",
        "card_name": "ELITE",
        "card_type": "premium",
        "annual_fee": 4999,
        "renewal_fee": 4999,
        "interest_rate": 39.0,
        "min_credit_score": 750,
        "min_income": 1800000,
        "welcome_benefits": {
            "reward_points": 10000,
            "milestone_bonus": "10000 bonus points on spending ₹2,00,000"
        },
        "reward_points": {
            "regular_spend": 5,
            "premium_spend": 10,
            "max_points": 20000
        },
        "cashback_details": {
            "regular": "1.5% on all spends",
            "special": "5% on luxury shopping"
        },
        "travel_benefits": {
            "lounge_access": "Unlimited international lounge access",
            "insurance": "Travel insurance up to ₹1 crore"
        },
        "lifestyle_benefits": {
            "concierge": "24/7 concierge services",
            "golf": "Complimentary golf rounds"
        }
    },
    {
        "bank_name": "Axis Bank",
        "card_name": "Flipkart Axis Bank",
        "card_type": "shopping",
        "annual_fee": 500,
        "renewal_fee": 500,
        "interest_rate": 40.0,
        "min_credit_score": 650,
        "min_income": 360000,
        "welcome_benefits": {
            "flipkart_voucher": "₹1500 Flipkart gift voucher",
            "reward_points": 1000
        },
        "reward_points": {
            "flipkart_spend": 5,
            "regular_spend": 2,
            "max_points": 5000
        },
        "cashback_details": {
            "flipkart": "5% unlimited cashback on Flipkart",
            "regular": "1% on other spends"
        },
        "travel_benefits": {
            "lounge_access": "2 domestic lounge visits per quarter",
            "fuel_surcharge": "1% fuel surcharge waiver"
        },
        "lifestyle_benefits": {
            "dining": "1+1 at select restaurants",
            "movies": "Buy 1 Get 1 on movie tickets"
        }
    },
    {
        "bank_name": "Standard Chartered",
        "card_name": "Ultimate",
        "card_type": "premium",
        "annual_fee": 5000,
        "renewal_fee": 5000,
        "interest_rate": 38.4,
        "min_credit_score": 750,
        "min_income": 2400000,
        "welcome_benefits": {
            "reward_points": 15000,
            "bonus": "₹10,000 cashback on spending ₹3,00,000"
        },
        "reward_points": {
            "regular_spend": 6,
            "premium_spend": 12,
            "max_points": "Unlimited"
        },
        "cashback_details": {
            "regular": "2% on all spends",
            "special": "10% on international transactions"
        },
        "travel_benefits": {
            "lounge_access": "Unlimited global lounge access",
            "insurance": "Multi-trip travel insurance"
        },
        "lifestyle_benefits": {
            "concierge": "Global concierge service",
            "privileges": "Priority Pass membership"
        }
    },
    {
        "bank_name": "Citi Bank",
        "card_name": "Prestige",
        "card_type": "travel",
        "annual_fee": 10000,
        "renewal_fee": 10000,
        "interest_rate": 37.2,
        "min_credit_score": 750,
        "min_income": 2500000,
        "welcome_benefits": {
            "air_miles": "10000 air miles",
            "hotel_voucher": "₹10,000 hotel credit"
        },
        "reward_points": {
            "travel_spend": 8,
            "regular_spend": 4,
            "max_points": 50000
        },
        "cashback_details": {
            "travel": "5% on flight bookings",
            "regular": "1.5% on other spends"
        },
        "travel_benefits": {
            "lounge_access": "Unlimited Priority Pass access",
            "insurance": "Comprehensive travel insurance"
        },
        "lifestyle_benefits": {
            "dining": "Global dining privileges",
            "hotels": "4th night free at luxury hotels"
        }
    },
    {
        "bank_name": "Yes Bank",
        "card_name": "First Exclusive",
        "card_type": "lifestyle",
        "annual_fee": 2499,
        "renewal_fee": 2499,
        "interest_rate": 40.8,
        "min_credit_score": 700,
        "min_income": 1200000,
        "welcome_benefits": {
            "reward_points": 8000,
            "vouchers": "₹5,000 lifestyle vouchers"
        },
        "reward_points": {
            "regular_spend": 3,
            "premium_spend": 6,
            "max_points": 15000
        },
        "cashback_details": {
            "regular": "1.2% on all spends",
            "special": "3% on weekend spends"
        },
        "travel_benefits": {
            "lounge_access": "12 lounge visits per year",
            "insurance": "Travel insurance up to ₹75 lakhs"
        },
        "lifestyle_benefits": {
            "dining": "Up to 25% off at partner restaurants",
            "wellness": "Complimentary gym memberships"
        }
    },
    {
        "bank_name": "RBL Bank",
        "card_name": "World Safari",
        "card_type": "travel",
        "annual_fee": 2000,
        "renewal_fee": 2000,
        "interest_rate": 41.4,
        "min_credit_score": 675,
        "min_income": 600000,
        "welcome_benefits": {
            "reward_points": 5000,
            "travel_voucher": "₹2,000 travel voucher"
        },
        "reward_points": {
            "travel_spend": 6,
            "regular_spend": 2,
            "max_points": 10000
        },
        "cashback_details": {
            "travel": "3% on travel bookings",
            "regular": "0.8% on other spends"
        },
        "travel_benefits": {
            "lounge_access": "8 international lounge visits",
            "insurance": "Travel insurance up to ₹25 lakhs"
        },
        "lifestyle_benefits": {
            "dining": "15% off at partner restaurants",
            "movies": "25% off on movie tickets"
        }
    },
    {
        "bank_name": "IndusInd Bank",
        "card_name": "Pinnacle",
        "card_type": "premium",
        "annual_fee": 7500,
        "renewal_fee": 7500,
        "interest_rate": 39.6,
        "min_credit_score": 750,
        "min_income": 3000000,
        "welcome_benefits": {
            "reward_points": 20000,
            "luxury_voucher": "₹15,000 luxury shopping voucher"
        },
        "reward_points": {
            "regular_spend": 7,
            "premium_spend": 14,
            "max_points": "Unlimited"
        },
        "cashback_details": {
            "regular": "2.5% on all spends",
            "luxury": "7% on luxury purchases"
        },
        "travel_benefits": {
            "lounge_access": "Unlimited global lounge access",
            "insurance": "Multi-trip insurance up to ₹2 crores"
        },
        "lifestyle_benefits": {
            "concierge": "24/7 lifestyle concierge",
            "golf": "Unlimited golf access"
        }
    },
    {
        "bank_name": "Kotak Mahindra",
        "card_name": "Royale Signature",
        "card_type": "lifestyle",
        "annual_fee": 2999,
        "renewal_fee": 2999,
        "interest_rate": 40.2,
        "min_credit_score": 700,
        "min_income": 1000000,
        "welcome_benefits": {
            "reward_points": 7500,
            "cashback": "₹3,000 welcome cashback"
        },
        "reward_points": {
            "regular_spend": 4,
            "premium_spend": 8,
            "max_points": 12000
        },
        "cashback_details": {
            "regular": "1.5% on all spends",
            "special": "4% on weekend dining"
        },
        "travel_benefits": {
            "lounge_access": "12 domestic lounge visits",
            "insurance": "Travel insurance up to ₹50 lakhs"
        },
        "lifestyle_benefits": {
            "dining": "20% off at partner restaurants",
            "spa": "Buy 1 Get 1 at luxury spas"
        }
    }
]

# Sample updates and offers
updates = [
    {
        "card_name": "HDFC Bank Regalia First",
        "update_type": "offer",
        "title": "5X Rewards on Amazon",
        "description": "Earn 5X reward points on all Amazon purchases above ₹5,000 this festive season",
        "valid_days": 30
    },
    {
        "card_name": "ICICI Bank Amazon Pay Signature",
        "update_type": "offer",
        "title": "10% Extra Cashback",
        "description": "Get additional 10% cashback on Amazon.in purchases above ₹10,000",
        "valid_days": 15
    },
    {
        "card_name": "SBI Card ELITE",
        "update_type": "feature_update",
        "title": "Enhanced Travel Benefits",
        "description": "Now enjoy complimentary access to 1000+ airport lounges worldwide",
        "valid_days": 60
    },
    {
        "card_name": "Axis Bank Flipkart Axis Bank",
        "update_type": "offer",
        "title": "Big Billion Days Special",
        "description": "Earn unlimited 10% cashback during Flipkart's Big Billion Days Sale",
        "valid_days": 7
    },
    {
        "card_name": "Standard Chartered Ultimate",
        "update_type": "promotion",
        "title": "Zero Annual Fee",
        "description": "Get annual fee waiver on spending ₹5,00,000 in first 90 days",
        "valid_days": 90
    },
    {
        "card_name": "Citi Bank Prestige",
        "update_type": "offer",
        "title": "Double Miles Offer",
        "description": "Earn double air miles on all international flight bookings",
        "valid_days": 45
    },
    {
        "card_name": "Yes Bank First Exclusive",
        "update_type": "feature_update",
        "title": "Enhanced Dining Program",
        "description": "Now enjoy up to 40% off at 1000+ premium restaurants",
        "valid_days": 30
    },
    {
        "card_name": "RBL Bank World Safari",
        "update_type": "offer",
        "title": "Travel Season Special",
        "description": "Flat 10% off on international hotel bookings via RBL portal",
        "valid_days": 60
    },
    {
        "card_name": "IndusInd Bank Pinnacle",
        "update_type": "promotion",
        "title": "Luxury Shopping Festival",
        "description": "Get up to 20% off at premium lifestyle brands",
        "valid_days": 21
    },
    {
        "card_name": "Kotak Mahindra Royale Signature",
        "update_type": "offer",
        "title": "Weekend Dining Delight",
        "description": "Earn 10X rewards on weekend dining, including food delivery",
        "valid_days": 30
    }
]

def add_sample_data():
    db = SessionLocal()
    try:
        # Clear existing data
        print("Clearing existing data...")
        db.query(CreditCardUpdate).delete()
        db.query(CreditCard).delete()
        db.commit()

        # Add credit cards
        print("Adding credit cards...")
        card_objects = []
        for card_data in credit_cards:
            # Convert dictionary fields to JSON strings
            card_data = card_data.copy()  # Create a copy to avoid modifying the original
            for field in ['welcome_benefits', 'reward_points', 'cashback_details', 
                         'travel_benefits', 'lifestyle_benefits']:
                if field in card_data and card_data[field]:
                    card_data[field] = convert_to_json_string(card_data[field])
            
            try:
                card = CreditCard(**card_data)
                db.add(card)
                card_objects.append(card)
                print(f"Added card: {card_data['bank_name']} {card_data['card_name']}")
            except Exception as e:
                print(f"Error adding card {card_data['bank_name']} {card_data['card_name']}: {str(e)}")
                raise
        
        db.commit()
        print(f"Added {len(card_objects)} credit cards successfully!")

        # Add updates
        print("\nAdding updates...")
        now = datetime.now()
        update_count = 0
        for update_data in updates:
            try:
                # Print all card names for debugging
                print(f"\nLooking for card: {update_data['card_name']}")
                print("Available cards:")
                for card in card_objects:
                    print(f"- {card.bank_name} {card.card_name}")
                
                card = next(card for card in card_objects 
                          if f"{card.bank_name} {card.card_name}" == update_data["card_name"])
                update = CreditCardUpdate(
                    card_id=card.id,
                    update_type=update_data["update_type"],
                    title=update_data["title"],
                    description=update_data["description"],
                    valid_from=now,
                    valid_until=now + timedelta(days=update_data["valid_days"]),
                    is_active=True
                )
                db.add(update)
                update_count += 1
                print(f"Added update for {update_data['card_name']}")
            except StopIteration:
                print(f"Error: Could not find card with name: {update_data['card_name']}")
                raise Exception(f"Card not found: {update_data['card_name']}")
            except Exception as e:
                print(f"Error adding update for {update_data['card_name']}: {str(e)}")
                raise

        db.commit()
        print(f"\nAdded {update_count} updates successfully!")

    except Exception as e:
        print(f"Error adding sample data: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    try:
        add_sample_data()
        print("Sample data added successfully!")
    except Exception as e:
        print(f"Failed to add sample data: {str(e)}") 