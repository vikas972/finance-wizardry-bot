from database import SessionLocal
import models

def create_test_customer():
    db = SessionLocal()
    try:
        # Create a test customer
        customer = models.Customer(
            name="Test User",
            email="test@example.com"
        )
        db.add(customer)
        db.commit()
        print(f"Created customer: {customer.name} (ID: {customer.id})")
    except Exception as e:
        print(f"Error creating customer: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_customer() 