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

@app.get("/customers/", response_model=List[schemas.Customer])
def read_customers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    customers = db.query(models.Customer).offset(skip).limit(limit).all()
    return customers

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
        
        # Prepare financial context with markdown formatting
        financial_context = {
            "customer_info": {
                "name": customer.name,
                "email": customer.email
            }
        }
        
        context_markdown = "## Financial Information\n\n"
        
        # Add AA data if available
        if customer.aa_data:
            latest_aa = customer.aa_data[-1]
            financial_context["account_info"] = {
                "account_summary": latest_aa.account_summary,
                "spending_patterns": latest_aa.spending_patterns,
                "assets": latest_aa.assets
            }
            context_markdown += "### Account Information\n"
            if latest_aa.account_summary.get("savings_account"):
                context_markdown += f"- **Current Balance**: ₹{latest_aa.account_summary['savings_account'].get('balance', 0):,.2f}\n"
            if latest_aa.spending_patterns:
                context_markdown += "#### Monthly Spending\n"
                for category, amount in latest_aa.spending_patterns.get("categories", {}).items():
                    context_markdown += f"- {category.title()}: ₹{amount:,.2f}\n"
        
        # Add bureau data if available
        if customer.bureau_data:
            latest_bureau = customer.bureau_data[-1]
            financial_context["credit_info"] = {
                "credit_score": latest_bureau.credit_score,
                "loan_details": latest_bureau.loan_details,
                "repayment_history": latest_bureau.repayment_history
            }
            context_markdown += "\n### Credit Information\n"
            context_markdown += f"- **Credit Score**: {latest_bureau.credit_score}\n"
            if latest_bureau.loan_details:
                context_markdown += "#### Active Loans\n"
                for loan_type, details in latest_bureau.loan_details.items():
                    context_markdown += f"**{loan_type.replace('_', ' ').title()}**:\n"
                    context_markdown += f"- Principal: ₹{details.get('principal', 0):,.2f}\n"
                    context_markdown += f"- Interest Rate: {details.get('interest_rate', 0)}%\n"
                    context_markdown += f"- Monthly EMI: ₹{details.get('monthly_emi', 0):,.2f}\n\n"
        
        # Add ITR data if available
        if customer.itr_data:
            latest_itr = customer.itr_data[-1]
            financial_context["tax_info"] = {
                "taxable_income": latest_itr.taxable_income,
                "tax_returns": latest_itr.tax_returns,
                "deductions": latest_itr.deductions
            }
            context_markdown += "\n### Tax Information\n"
            context_markdown += f"- **Annual Income**: ₹{latest_itr.taxable_income:,.2f}\n"
            if latest_itr.deductions:
                context_markdown += "#### Tax Deductions\n"
                for deduction_type, amount in latest_itr.deductions.items():
                    context_markdown += f"- {deduction_type}: ₹{amount:,.2f}\n"
        
        # Prepare messages for OpenAI with markdown formatting instruction
        system_message = """You are a financial advisor assistant. Analyze the provided financial data and answer questions.
        Format your responses using markdown for better readability:
        - Use ### for main sections
        - Use bullet points (- ) for lists
        - Use **bold** for important numbers and key points
        - Use ₹ symbol for Indian Rupee amounts
        - Format large numbers with commas for readability
        - Use tables where appropriate using markdown syntax
        
        Only use the information available in the context. If you don't have certain information, say so.
        Be specific and reference actual numbers from the data when available."""
        
        messages = [
            {"role": "system", "content": system_message},
            *conversation_history,
            {"role": "user", "content": f"{context_markdown}\n\nQuestion: {query}"}
        ]
        
        # Call OpenAI API
        try:
            response = openai.ChatCompletion.create(
                engine="gpt4o",
                messages=messages,
                max_tokens=4096,
                temperature=0.3
            )
            
            ai_response = response["choices"][0]["message"]["content"]
            
            return {
                "query": query,
                "response": ai_response,
                "financial_context": financial_context
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