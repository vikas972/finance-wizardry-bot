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
├── backend/              # FastAPI backend
│   ├── models.py        # Database models
│   ├── schemas.py       # Pydantic schemas
│   ├── main.py         # Main FastAPI application
│   └── requirements.txt # Python dependencies
└── frontend/           # React/TypeScript frontend
    ├── src/           # Source code
    ├── package.json   # Node dependencies
    └── vite.config.ts # Vite configuration
```

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
- OpenAI API
- sentence-transformers

## Troubleshooting

1. Database Connection Issues:
   - Verify PostgreSQL is running
   - Check database credentials in .env
   - Ensure database 'customer_info' exists

2. OpenAI API Issues:
   - Verify API key in .env
   - Check API endpoint configuration

3. CORS Issues:
   - Backend is configured to accept requests from localhost:5173
   - If using different ports, update CORS settings in main.py
