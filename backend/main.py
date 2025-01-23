from fastapi import FastAPI, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import models
import schemas
from database import engine, get_db
from fastapi.middleware.cors import CORSMiddleware
from rag_utils import RAGPipeline
import openai
import json
from pydantic import BaseModel
from datetime import datetime

# OpenAI Azure Configuration
openai.api_type = "azure"
openai.api_base = "https://eastusigtb.openai.azure.com/"
openai.api_version = "2024-02-15-preview"
openai.api_key = "34a93b9dd2bc45ef8d6f07e5ef92940e"

models.Base.metadata.create_all(bind=engine)
rag_pipeline = RAGPipeline()

app = FastAPI()

# Configure CORS - more permissive configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # More permissive for development
    allow_credentials=False,  # Changed to False since we're using allow_origins=["*"]
    allow_methods=["*"],
    allow_headers=["*"]
)

# Add OPTIONS handler for the chat endpoint
@app.options("/customers/{customer_id}/chat/")
async def chat_options():
    return {"message": "OK"}

# Add a test endpoint to verify API is working
@app.get("/")
def read_root():
    return {"message": "API is working!"}

class ChatMessage(BaseModel):
    query: str
    conversation_history: List[Dict[str, str]] = []

@app.post("/customers/", response_model=schemas.Customer)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    db_customer = models.Customer(name=customer.name, email=customer.email)
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

@app.get("/customers/")
async def read_customers(db: Session = Depends(get_db)):
    try:
        customers = db.query(models.Customer).all()
        return [
            {
                "id": customer.id,
                "name": customer.name,
                "email": customer.email,
                "created_at": customer.created_at.isoformat()
            }
            for customer in customers
        ]
    except Exception as e:
        print(f"Error fetching customers: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/customers/{customer_id}", response_model=schemas.Customer)
def read_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@app.post("/customers/{customer_id}/transactions/", response_model=schemas.Transaction)
def create_transaction(
    customer_id: int, transaction: schemas.TransactionCreate, db: Session = Depends(get_db)
):
    customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    db_transaction = models.Transaction(
        **transaction.dict(), customer_id=customer_id
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@app.get("/customers/{customer_id}/transactions/", response_model=List[schemas.Transaction])
def read_customer_transactions(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer.transactions 

@app.post("/customers/{customer_id}/aa-data/", response_model=schemas.AAData)
def create_aa_data(customer_id: int, aa_data: schemas.AADataCreate, db: Session = Depends(get_db)):
    customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # Generate text embedding
    text = rag_pipeline.prepare_aa_data_text(aa_data.dict())
    vector_embedding = rag_pipeline.generate_embedding(text)
    
    db_aa_data = models.AAData(**aa_data.dict(), customer_id=customer_id, vector_embedding=vector_embedding)
    db.add(db_aa_data)
    db.commit()
    db.refresh(db_aa_data)
    return db_aa_data

@app.post("/customers/{customer_id}/bureau-data/", response_model=schemas.BureauData)
def create_bureau_data(customer_id: int, bureau_data: schemas.BureauDataCreate, db: Session = Depends(get_db)):
    customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # Generate text embedding
    text = rag_pipeline.prepare_bureau_data_text(bureau_data.dict())
    vector_embedding = rag_pipeline.generate_embedding(text)
    
    db_bureau_data = models.BureauData(**bureau_data.dict(), customer_id=customer_id, vector_embedding=vector_embedding)
    db.add(db_bureau_data)
    db.commit()
    db.refresh(db_bureau_data)
    return db_bureau_data

@app.post("/customers/{customer_id}/itr-data/", response_model=schemas.ITRData)
def create_itr_data(customer_id: int, itr_data: schemas.ITRDataCreate, db: Session = Depends(get_db)):
    customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # Generate text embedding
    text = rag_pipeline.prepare_itr_data_text(itr_data.dict())
    vector_embedding = rag_pipeline.generate_embedding(text)
    
    db_itr_data = models.ITRData(**itr_data.dict(), customer_id=customer_id, vector_embedding=vector_embedding)
    db.add(db_itr_data)
    db.commit()
    db.refresh(db_itr_data)
    return db_itr_data

@app.post("/customers/{customer_id}/query/")
def query_customer_data(
    customer_id: int,
    query: str,
    db: Session = Depends(get_db)
):
    customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # Collect all customer documents
    documents = []
    
    # Add AA data
    for aa_data in customer.aa_data:
        doc = aa_data.__dict__
        doc['type'] = 'aa_data'
        documents.append(doc)
    
    # Add Bureau data
    for bureau_data in customer.bureau_data:
        doc = bureau_data.__dict__
        doc['type'] = 'bureau_data'
        documents.append(doc)
    
    # Add ITR data
    for itr_data in customer.itr_data:
        doc = itr_data.__dict__
        doc['type'] = 'itr_data'
        documents.append(doc)
    
    # Retrieve relevant documents
    relevant_docs = rag_pipeline.retrieve_relevant_documents(query, documents)
    
    # Prepare context for GPT-4
    context = "Here is the relevant financial information:\n\n"
    for doc in relevant_docs:
        context += f"Document Type: {doc['type']}\n"
        if doc['type'] == 'aa_data':
            context += f"Account Summary: {json.dumps(doc['account_summary'], indent=2)}\n"
            context += f"Spending Patterns: {json.dumps(doc['spending_patterns'], indent=2)}\n"
            context += f"Assets: {json.dumps(doc['assets'], indent=2)}\n"
        elif doc['type'] == 'bureau_data':
            context += f"Loan Details: {json.dumps(doc['loan_details'], indent=2)}\n"
            context += f"Credit Score: {doc['credit_score']}\n"
            context += f"Repayment History: {json.dumps(doc['repayment_history'], indent=2)}\n"
        elif doc['type'] == 'itr_data':
            context += f"Tax Returns: {json.dumps(doc['tax_returns'], indent=2)}\n"
            context += f"Taxable Income: {doc['taxable_income']}\n"
            context += f"Deductions: {json.dumps(doc['deductions'], indent=2)}\n"
        context += "\n---\n"

    # Prepare prompt for GPT-4
    prompt = """You are a financial advisor assistant. Using the provided financial information, 
    answer the user's query accurately and professionally. Only use the information provided in 
    the context. If you cannot find relevant information to answer the query, please state that clearly."""

    # Call GPT-4
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": f"Context:\n{context}\n\nQuery: {query}"}
    ]

    response = openai.ChatCompletion.create(
        engine="gpt4o",
        messages=messages,
        max_tokens=4096,
        temperature=0
    )

    ai_response = response["choices"][0]["message"]["content"]
    
    return {
        "query": query,
        "relevant_documents": relevant_docs,
        "ai_response": ai_response
    } 

@app.post("/customers/{customer_id}/chat/")
async def chat_with_customer_data(
    customer_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    try:
        # Parse the request body
        body = await request.json()
        query = body.get("query", "")
        conversation_history = body.get("conversation_history", [])

        # Validate required fields
        if not query:
            raise HTTPException(status_code=400, detail="Query is required")

        # Get customer data
        customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        # Get all relevant financial data
        latest_aa = customer.aa_data[-1] if customer.aa_data else None
        latest_bureau = customer.bureau_data[-1] if customer.bureau_data else None
        latest_itr = customer.itr_data[-1] if customer.itr_data else None
        loan_metrics = customer.loan_eligibility_metrics
        credit_preferences = customer.credit_card_preferences
        recent_transactions = customer.transactions[-5:] if customer.transactions else []  # Last 5 transactions

        # Prepare comprehensive financial context with markdown formatting
        context_markdown = "## Customer Profile\n\n"
        
        # Basic Info and Demographics
        context_markdown += f"### Personal Information\n"
        context_markdown += f"- Name: {customer.name}\n"
        context_markdown += f"- Age: {customer.age}\n"
        context_markdown += f"- Occupation: {customer.occupation}\n"
        if customer.interests:
            context_markdown += f"- Interests: {', '.join(customer.interests)}\n"
        if customer.lifestyle_preferences:
            context_markdown += "\n#### Lifestyle Preferences\n"
            for category, preference in customer.lifestyle_preferences.items():
                context_markdown += f"- {category.replace('_', ' ').title()}: {preference}\n"
        
        # Credit and Loan Information
        if latest_bureau:
            context_markdown += f"\n### Credit Profile\n"
            context_markdown += f"- Credit Score: **{latest_bureau.credit_score}**\n"
            if latest_bureau.loan_details:
                context_markdown += "#### Active Loans\n"
                for loan_type, details in latest_bureau.loan_details.items():
                    context_markdown += f"- {loan_type.replace('_', ' ').title()}:\n"
                    context_markdown += f"  * Principal: ₹{details.get('principal', 0):,.2f}\n"
                    context_markdown += f"  * Remaining: ₹{details.get('remaining', 0):,.2f}\n"
                    context_markdown += f"  * EMI: ₹{details.get('monthly_emi', 0):,.2f}\n"

        # Income and Tax Information
        if latest_itr:
            context_markdown += f"\n### Income Details\n"
            context_markdown += f"- Annual Income: ₹{latest_itr.taxable_income:,.2f}\n"
            context_markdown += f"- Monthly Income: ₹{latest_itr.taxable_income/12:,.2f}\n"
            if latest_itr.deductions:
                context_markdown += "#### Tax Deductions\n"
                for deduction_type, amount in latest_itr.deductions.items():
                    context_markdown += f"- {deduction_type}: ₹{amount:,.2f}\n"

        # Account and Spending Information
        if latest_aa:
            context_markdown += f"\n### Banking Details\n"
            if latest_aa.account_summary.get("savings_account"):
                context_markdown += f"- Current Balance: ₹{latest_aa.account_summary['savings_account'].get('balance', 0):,.2f}\n"
                context_markdown += f"- Monthly Average: ₹{latest_aa.account_summary['savings_account'].get('monthly_average', 0):,.2f}\n"
            
            if latest_aa.spending_patterns:
                context_markdown += "\n#### Monthly Spending Patterns\n"
                for category, amount in latest_aa.spending_patterns.get("categories", {}).items():
                    context_markdown += f"- {category.title()}: ₹{amount:,.2f}\n"

        # Loan Eligibility Metrics
        if loan_metrics:
            context_markdown += f"\n### Loan Eligibility Status\n"
            context_markdown += f"- Eligibility Score: **{loan_metrics.eligibility_score}** ({loan_metrics.score_range})\n"
            context_markdown += f"- Debt-to-Income Ratio: {loan_metrics.debt_to_income_ratio:.1f}% ({loan_metrics.dti_status})\n"
            context_markdown += f"- Current EMI Load: ₹{loan_metrics.current_emi_load:,.2f} ({loan_metrics.emi_status})\n"

        # Credit Card Preferences
        if credit_preferences:
            context_markdown += f"\n### Credit Card Preferences\n"
            context_markdown += f"- Preferred Categories: {', '.join(credit_preferences.preferred_categories)}\n"
            context_markdown += f"- Max Annual Fee: ₹{credit_preferences.max_annual_fee:,.2f}\n"
            context_markdown += f"- Reward Type: {credit_preferences.preferred_reward_type}\n"
            context_markdown += f"- Travel Frequency: {credit_preferences.travel_frequency}\n"
        
        # Prepare system message with instructions
        system_message = """You are an AI financial advisor with access to the customer's comprehensive financial data. 
        When answering questions:
        1. Consider the customer's age, occupation, and interests for personalized recommendations
        2. Factor in their lifestyle preferences and spending patterns
        3. Always reference specific numbers and data points from their profile
        4. Provide personalized advice based on their actual financial situation
        5. Consider their credit score, income, spending patterns, and existing obligations
        6. For credit card recommendations:
           - Match cards to their interests (travel/dining/shopping)
           - Consider their spending patterns and reward preferences
           - Factor in their age and lifestyle for relevant perks
           - Ensure recommendations align with their credit score and income
        7. Format responses using markdown for better readability
        8. Use ₹ symbol for Indian Rupee amounts
        9. Format large numbers with commas
        10. Use bullet points for lists
        11. Bold important numbers and conclusions
        
        If you don't have certain information in the context, acknowledge that limitation in your response."""

        # Prepare messages for OpenAI
        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"Customer Financial Context:\n{context_markdown}\n\nPrevious Conversation:\n"},
            *conversation_history[-4:],  # Include last 4 messages for context
            {"role": "user", "content": query}
        ]
        
        # Call OpenAI API
        try:
            response = openai.ChatCompletion.create(
                engine="gpt4o",
                messages=messages,
                max_tokens=4096,
                temperature=0.3
            )
            
            ai_response = response.choices[0].message.content
            
            return {
                "query": query,
                "response": ai_response,
                "financial_context": {
                    "credit_score": latest_bureau.credit_score if latest_bureau else None,
                    "monthly_income": latest_itr.taxable_income/12 if latest_itr else None,
                    "current_balance": latest_aa.account_summary.get("savings_account", {}).get("balance") if latest_aa else None,
                    "demographics": {
                        "age": customer.age,
                        "occupation": customer.occupation,
                        "interests": customer.interests,
                        "lifestyle_preferences": customer.lifestyle_preferences
                    } if customer else None,
                    "loan_eligibility": {
                        "score": loan_metrics.eligibility_score if loan_metrics else None,
                        "status": loan_metrics.score_range if loan_metrics else None
                    } if loan_metrics else None
                }
            }
            
        except Exception as e:
            print(f"OpenAI API Error: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Error generating response from AI service"
            )
            
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Server Error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@app.get("/debug/customer/{customer_id}")
async def debug_customer_data(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    return {
        "customer": {
            "id": customer.id,
            "name": customer.name,
            "email": customer.email
        },
        "aa_data": [data.__dict__ for data in customer.aa_data],
        "bureau_data": [data.__dict__ for data in customer.bureau_data],
        "itr_data": [data.__dict__ for data in customer.itr_data],
        "transactions": [t.__dict__ for t in customer.transactions]
    } 

@app.get("/customers/{customer_id}/loan-eligibility")
def get_loan_eligibility(customer_id: int, db: Session = Depends(get_db)):
    # Get the customer's loan eligibility metrics
    metrics = db.query(models.LoanEligibilityMetrics).filter(
        models.LoanEligibilityMetrics.customer_id == customer_id
    ).first()
    
    if not metrics:
        raise HTTPException(status_code=404, detail="Loan eligibility metrics not found")
    
    return {
        "eligibility_score": metrics.eligibility_score,
        "score_range": metrics.score_range,
        "debt_to_income_ratio": metrics.debt_to_income_ratio,
        "dti_status": metrics.dti_status,
        "current_emi_load": metrics.current_emi_load,
        "emi_status": metrics.emi_status
    } 

@app.get("/credit-cards/")
def get_credit_cards(db: Session = Depends(get_db)):
    """Get all available credit cards"""
    cards = db.query(models.CreditCard).all()
    return cards

@app.get("/customers/{customer_id}/credit-card-preferences")
def get_customer_credit_card_preferences(customer_id: int, db: Session = Depends(get_db)):
    """Get customer's credit card preferences"""
    preferences = db.query(models.CustomerCreditCardPreference).filter(
        models.CustomerCreditCardPreference.customer_id == customer_id
    ).first()
    if not preferences:
        raise HTTPException(status_code=404, detail="Credit card preferences not found")
    return preferences

@app.post("/customers/{customer_id}/credit-card-preferences")
def update_credit_card_preferences(
    customer_id: int,
    preferences: dict,
    db: Session = Depends(get_db)
):
    """Update customer's credit card preferences"""
    existing_preferences = db.query(models.CustomerCreditCardPreference).filter(
        models.CustomerCreditCardPreference.customer_id == customer_id
    ).first()

    if existing_preferences:
        for key, value in preferences.items():
            setattr(existing_preferences, key, value)
    else:
        preferences["customer_id"] = customer_id
        new_preferences = models.CustomerCreditCardPreference(**preferences)
        db.add(new_preferences)

    db.commit()
    return {"message": "Preferences updated successfully"}

@app.post("/customers/{customer_id}/recommend-credit-cards")
async def recommend_credit_cards(customer_id: int, db: Session = Depends(get_db)):
    """Get personalized credit card recommendations"""
    # Get customer data
    customer = db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    # Get customer's financial data
    bureau_data = customer.bureau_data[-1] if customer.bureau_data else None
    itr_data = customer.itr_data[-1] if customer.itr_data else None
    preferences = customer.credit_card_preferences

    if not all([bureau_data, itr_data, preferences]):
        raise HTTPException(
            status_code=400,
            detail="Insufficient data for recommendations"
        )

    # Get all credit cards
    credit_cards = db.query(models.CreditCard).all()

    # Prepare context for GPT-4
    context = f"""
    Customer Profile:
    - Monthly Income: ₹{itr_data.taxable_income / 12:,.2f}
    - Credit Score: {bureau_data.credit_score}
    - Preferred Categories: {preferences.preferred_categories}
    - Maximum Annual Fee: ₹{preferences.max_annual_fee:,.2f}
    - Preferred Reward Type: {preferences.preferred_reward_type}
    - Travel Frequency: {preferences.travel_frequency}
    - Current Cards: {preferences.current_cards}
    - Monthly Spending Patterns: {preferences.monthly_spending}

    Available Credit Cards:
    """
    
    for card in credit_cards:
        context += f"""
        {card.bank_name} {card.card_name}:
        - Type: {card.card_type}
        - Annual Fee: ₹{card.annual_fee}
        - Min Income Required: ₹{card.min_income}
        - Min Credit Score: {card.min_credit_score}
        - Key Benefits:
          * Welcome: {card.welcome_benefits}
          * Rewards: {card.reward_points}
          * Cashback: {card.cashback_details}
          * Travel: {card.travel_benefits}
          * Lifestyle: {card.lifestyle_benefits}
        """

    # Prepare prompt for GPT-4
    prompt = """You are a credit card recommendation expert. Based on the customer's profile and preferences, 
    analyze the available credit cards and recommend the best options. Consider:
    1. Eligibility (income and credit score requirements)
    2. Match with spending patterns and lifestyle preferences
    3. Value for money (benefits vs annual fee)
    4. Complementary benefits to existing cards

    Provide a ranked list of top 3 recommended cards with detailed justification for each recommendation.
    Format your response in markdown with clear sections and bullet points."""

    try:
        response = openai.ChatCompletion.create(
            engine="gpt4o",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": f"Context:\n{context}\n\nProvide credit card recommendations for this customer."}
            ],
            max_tokens=4096,
            temperature=0.3
        )

        recommendations = response.choices[0].message.content

        return {
            "customer_profile": {
                "monthly_income": itr_data.taxable_income / 12,
                "credit_score": bureau_data.credit_score,
                "preferences": preferences
            },
            "recommendations": recommendations
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating recommendations: {str(e)}"
        ) 

@app.get("/credit-cards/updates")
def get_credit_card_updates(db: Session = Depends(get_db)):
    """Get all active credit card updates and offers"""
    current_time = datetime.now()
    updates = db.query(models.CreditCardUpdate).filter(
        models.CreditCardUpdate.is_active == True,
        models.CreditCardUpdate.valid_from <= current_time,
        models.CreditCardUpdate.valid_until >= current_time
    ).all()
    
    # Group updates by card
    grouped_updates = {}
    for update in updates:
        if update.card_id not in grouped_updates:
            grouped_updates[update.card_id] = {
                "card": {
                    "bank_name": update.credit_card.bank_name,
                    "card_name": update.credit_card.card_name,
                },
                "updates": []
            }
        grouped_updates[update.card_id]["updates"].append({
            "id": update.id,
            "type": update.update_type,
            "title": update.title,
            "description": update.description,
            "valid_until": update.valid_until.isoformat()
        })
    
    return grouped_updates

@app.get("/credit-cards/{card_id}/updates")
def get_card_updates(card_id: int, db: Session = Depends(get_db)):
    """Get updates for a specific credit card"""
    current_time = datetime.now()
    updates = db.query(models.CreditCardUpdate).filter(
        models.CreditCardUpdate.card_id == card_id,
        models.CreditCardUpdate.is_active == True,
        models.CreditCardUpdate.valid_from <= current_time,
        models.CreditCardUpdate.valid_until >= current_time
    ).all()
    
    return [
        {
            "id": update.id,
            "type": update.update_type,
            "title": update.title,
            "description": update.description,
            "valid_from": update.valid_from.isoformat(),
            "valid_until": update.valid_until.isoformat()
        }
        for update in updates
    ]

@app.post("/credit-cards/{card_id}/updates")
def create_card_update(
    card_id: int,
    update: dict,
    db: Session = Depends(get_db)
):
    """Create a new update or offer for a credit card"""
    db_update = models.CreditCardUpdate(
        card_id=card_id,
        **update
    )
    db.add(db_update)
    db.commit()
    db.refresh(db_update)
    return db_update 