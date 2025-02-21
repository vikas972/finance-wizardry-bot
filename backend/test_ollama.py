from llm_utils import OllamaLLM

# Initialize the LLM
llm = OllamaLLM(
    model_name="deepseek-r1:1.5b",  # or any other model you've pulled
    base_url="http://localhost:11434"
)

# Generate a response
response = llm.generate_response(
    prompt="What investment strategies would you recommend?",
    system_prompt="You are a financial advisor helping clients with investment decisions."
)

# Generate embeddings for semantic search
embeddings = llm.generate_embeddings("Some text to embed")

# Get financial advice with context
advice = llm.get_financial_advice(
    query="Should I invest in stocks?",
    customer_data={
        "income": 100000,
        "savings": 50000,
        "risk_profile": "moderate"
    }
)


print(advice)