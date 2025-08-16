#!/usr/bin/env python3
"""
Test script for multi-agent architecture
"""

import sys
import os

# Add current directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("🧪 Testing Multi-Agent Architecture...")
    print("=" * 50)
    
    # Test 1: Import agent modules
    print("\n1️⃣ Testing imports...")
    from agents.agent_coordinator import coordinator
    from agents.base_agent import AgentFactory
    from tools.database_tools import get_database_tools
    from config.agents_config import config
    print("✅ All imports successful!")
    
    # Test 2: Check agent initialization
    print("\n2️⃣ Testing agent initialization...")
    print(f"Available agents: {list(coordinator.agents.keys())}")
    print("✅ Agent coordinator initialized!")
    
    # Test 3: Check database tools
    print("\n3️⃣ Testing database tools...")
    tools = get_database_tools()
    print(f"Available tools: {[tool.name for tool in tools]}")
    print("✅ Database tools loaded!")
    
    # Test 4: Test agent creation
    print("\n4️⃣ Testing agent creation...")
    news_agent = coordinator.get_agent("news_intelligence")
    advisor_agent = coordinator.get_agent("financial_advisor")
    print(f"News Agent: {news_agent.agent.role}")
    print(f"Advisor Agent: {advisor_agent.agent.role}")
    print("✅ Agents created successfully!")
    
    # Test 5: Check configuration
    print("\n5️⃣ Testing configuration...")
    print(f"LLM Model: {config.default_model}")
    print(f"Ollama URL: {config.ollama_base_url}")
    print(f"Verbose: {config.verbose}")
    print("✅ Configuration loaded!")
    
    print("\n🎉 ALL TESTS PASSED!")
    print("Your multi-agent architecture is ready!")
    print("\nNext steps:")
    print("1. Start the backend: uvicorn main:app --reload --host 0.0.0.0 --port 3000")
    print("2. Test the new endpoints:")
    print("   - GET /agents/available")
    print("   - GET /agents/workflows") 
    print("   - POST /agents/chat/{agent_type}")
    print("   - POST /customers/{customer_id}/chat-agent/")

except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure all dependencies are installed:")
    print("pip install crewai crewai-tools pydantic-settings langchain-openai")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("Please check the configuration and dependencies.")
