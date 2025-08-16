# Finance Wizardry Bot

An AI-powered financial advisor chatbot that helps users with personalized financial guidance, loan analysis, and investment recommendations.

## Features

- Interactive AI Chat Assistant
- Financial Dashboard with Metrics and Charts
- Product-specific Financial Advice
- Real-time Data Analysis
- Tax Planning Assistance

## Prerequisites

- Node.js (v16 or higher)
- Python (3.8 or higher)
- PostgreSQL (13 or higher)
- npm or yarn package manager

## Project Structure

```
finance-wizardry-bot/
├── backend/                    # FastAPI backend
│   ├── models.py              # Database models
│   ├── schemas.py             # Pydantic schemas
│   ├── main.py                # Main FastAPI application
│   ├── simple_agents.py       # Working multi-agent system
│   ├── requirements.txt       # Python dependencies
│   │
│   ├── core/                  # Core services
│   │   └── services/
│   │       └── llm_service.py # Ollama LLM integration
│   │
│   ├── config/                # Configuration management
│   │   └── app_config.py      # Centralized app configuration
│   │
│   └── [EXPERIMENTAL]         # ⚠️  NOT CURRENTLY USED - TESTING REQUIRED
│       ├── agents/            # Old CrewAI implementation (OBSOLETE)
│       ├── tools/             # Old database tools (OBSOLETE)
│       └── config/agents_config.py # Old agent config (OBSOLETE)
│
└── frontend/                  # React/TypeScript frontend
    ├── src/                   # Source code
    ├── package.json           # Node dependencies
    └── vite.config.ts         # Vite configuration
```

### 🔴 **IMPORTANT: Folder Usage Status**

#### ✅ **ACTIVELY USED (Production Ready)**
- `backend/models.py` - Database models
- `backend/schemas.py` - Pydantic schemas  
- `backend/main.py` - FastAPI application
- `backend/simple_agents.py` - Multi-agent system
- `backend/core/services/llm_service.py` - LLM integration
- `backend/config/app_config.py` - Configuration management

#### ⚠️ **NOT CURRENTLY USED (Future Testing Required)**
- `backend/agents/` - **OBSOLETE**: Old CrewAI implementation
- `backend/tools/` - **OBSOLETE**: Old database tools for CrewAI
- `backend/config/agents_config.py` - **OBSOLETE**: Replaced by app_config.py

#### 📋 **Future Implementation Guidelines**
Before using any folder marked as "NOT CURRENTLY USED":
1. **Test thoroughly** in development environment
2. **Verify compatibility** with current `simple_agents.py` system
3. **Update imports** and dependencies as needed
4. **Document changes** in this README
5. **Remove obsolete code** after successful migration

## Setup Instructions

### Backend Setup

1. Create and activate a Python virtual environment:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Set up PostgreSQL:
- Create a database named 'customer_info'
- Update .env file with your database credentials

4. Initialize the database:
```bash
python create_db.py
```

5. Start the backend server:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 3000
```

### Frontend Setup

1. Install Node.js dependencies:
```bash
cd ../  # Return to project root
npm install
```

2. Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:5173`

## Environment Variables

### Backend (.env)
```
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=customer_info

# OpenAI Configuration
OPENAI_API_TYPE=azure
OPENAI_API_BASE=https://eastusigtb.openai.azure.com/
OPENAI_API_VERSION=2024-02-15-preview
OPENAI_API_KEY=your_api_key
```

## API Documentation

Once the backend is running, you can access:
- API documentation: `http://localhost:3000/docs`
- Alternative documentation: `http://localhost:3000/redoc`

### **Available Endpoints:**

#### **Customer Management:**
- `GET /customers/` - List all customers
- `GET /customers/{customer_id}` - Get customer details
- `POST /customers/` - Create new customer
- `GET /customers/{customer_id}/transactions/` - Get customer transactions

#### **Multi-Agent System:**
- `POST /agents/chat/{agent_type}` - Chat with specific agent
- `POST /agents/workflow/comprehensive-analysis` - Run comprehensive analysis
- `POST /agents/workflow/investment-recommendation` - Get investment advice
- `POST /agents/workflow/market-analysis` - Market analysis
- `POST /agents/workflow/credit-optimization` - Credit optimization
- `GET /agents/available` - List available agents
- `GET /agents/workflows` - List available workflows

#### **News Intelligence:**
- `GET /news/` - Get latest news articles
- `GET /news/trending` - Get trending topics
- `GET /news/sentiment` - Get market sentiment analysis
- `GET /news/categories` - Get news categories

#### **Credit Cards:**
- `GET /credit-cards/` - List available credit cards
- `GET /customers/{customer_id}/credit-card-preferences` - Get preferences
- `POST /customers/{customer_id}/recommend-credit-cards` - Get recommendations

#### **AI Chat:**
- `POST /customers/{customer_id}/chat/` - Chat with AI assistant
- `POST /customers/{customer_id}/chat-agent/` - Chat with specific agent

## Available Scripts

Frontend:
- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build

Backend:
- `uvicorn main:app --reload` - Start development server
- `python create_db.py` - Initialize database
- `python sample_data.py` - Load sample data (optional)

## Tech Stack

Frontend:
- React
- TypeScript
- Vite
- Tailwind CSS
- shadcn/ui
- Recharts

Backend:
- FastAPI
- SQLAlchemy
- PostgreSQL
- Ollama LLM (replaced OpenAI)
- sentence-transformers

## 🏗️ **Current Architecture**

### **Multi-Agent System (simple_agents.py)**
- **News Intelligence Agent**: Real-time news fetching and sentiment analysis
- **Financial Advisor Agent**: Personalized financial advice using customer data
- **Credit Specialist Agent**: Credit analysis and optimization recommendations
- **Coordinator**: Intelligent query routing and workflow execution

### **Configuration Management (app_config.py)**
- Centralized environment variable management
- Ollama model configuration (global and agent-specific)
- UI color schemes and customization
- Database and security settings

### **LLM Integration (llm_service.py)**
- Ollama integration for dynamic AI responses
- Agent-specific model selection
- Context-aware financial advice generation

## 🔄 **Migration Notes**

### **What Changed:**
- **Replaced CrewAI** with simplified `simple_agents.py` system
- **Replaced OpenAI** with Ollama for local LLM processing
- **Centralized configuration** in `app_config.py`
- **Removed complex dependencies** for better maintainability

### **Why This Approach:**
- **Faster development** without dependency conflicts
- **Easier debugging** with simpler architecture
- **Better performance** with local LLM processing
- **Maintainable code** with clear separation of concerns

## Troubleshooting

1. Database Connection Issues:
   - Verify PostgreSQL is running
   - Check database credentials in .env
   - Ensure database 'customer_info' exists

2. Ollama LLM Issues:
   - Verify Ollama is running on `http://localhost:11434`
   - Check model availability: `ollama list`
   - Verify model configuration in `.env`

3. CORS Issues:
   - Backend is configured to accept requests from localhost:5173
   - If using different ports, update CORS settings in main.py

## 🚀 **Future Development Guidelines**

### **Adding New Features:**
1. **Use existing `simple_agents.py`** architecture for new agents
2. **Extend `models.py`** for new data requirements
3. **Add endpoints in `main.py`** following existing patterns
4. **Update `app_config.py`** for new configuration options

### **Testing Requirements:**
Before implementing any new feature:
1. **Unit tests** for new agent logic
2. **Integration tests** for API endpoints
3. **Database migration tests** for schema changes
4. **Performance tests** for LLM operations

### **Code Quality Standards:**
- **Type hints** for all Python functions
- **Error handling** with proper HTTP status codes
- **Logging** for debugging and monitoring
- **Documentation** for all new endpoints and agents

### **Security Considerations:**
- **Input validation** using Pydantic schemas
- **Authentication** for sensitive endpoints
- **Rate limiting** for LLM operations
- **Data encryption** for sensitive customer information
