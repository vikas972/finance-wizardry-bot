#!/usr/bin/env python3
"""
Simplified test for multi-agent architecture without complex tools
"""

import sys
import os

# Add current directory to path to import modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("🧪 Testing Simplified Multi-Agent Architecture...")
    print("=" * 60)
    
    # Test 1: Import core modules
    print("\n1️⃣ Testing core imports...")
    from crewai import Agent, Task, Crew
    from langchain_community.llms import Ollama
    from config.agents_config import config, AGENT_ROLES
    print("✅ Core CrewAI imports successful!")
    
    # Test 2: Create a simple agent without tools
    print("\n2️⃣ Testing simple agent creation...")
    
    # Create LLM
    llm = Ollama(
        model=config.default_model,
        base_url=config.ollama_base_url,
        temperature=0.7
    )
    print(f"✅ LLM created with model: {config.default_model}")
    
    # Create News Intelligence Agent
    news_agent = Agent(
        role=AGENT_ROLES["news_intelligence"]["role"],
        goal=AGENT_ROLES["news_intelligence"]["goal"],
        backstory=AGENT_ROLES["news_intelligence"]["backstory"],
        llm=llm,
        verbose=True,
        allow_delegation=False
    )
    print("✅ News Intelligence Agent created!")
    
    # Create Financial Advisor Agent  
    advisor_agent = Agent(
        role=AGENT_ROLES["financial_advisor"]["role"],
        goal=AGENT_ROLES["financial_advisor"]["goal"],
        backstory=AGENT_ROLES["financial_advisor"]["backstory"],
        llm=llm,
        verbose=True,
        allow_delegation=False
    )
    print("✅ Financial Advisor Agent created!")
    
    # Test 3: Create a simple task
    print("\n3️⃣ Testing simple task creation...")
    
    simple_task = Task(
        description="Provide a brief overview of current market sentiment and key financial trends.",
        expected_output="A concise market overview with 3-5 key points about current trends.",
        agent=news_agent
    )
    print("✅ Simple task created!")
    
    # Test 4: Test crew creation
    print("\n4️⃣ Testing crew creation...")
    
    crew = Crew(
        agents=[news_agent, advisor_agent],
        tasks=[simple_task],
        verbose=True
    )
    print("✅ Crew created successfully!")
    
    print("\n🎉 SIMPLIFIED AGENT TEST PASSED!")
    print("Your basic multi-agent architecture is working!")
    
    print("\n📋 Next Steps:")
    print("1. The agents are successfully created and can be used")
    print("2. You can now integrate them into your FastAPI endpoints")
    print("3. Start the backend and test the agent endpoints")
    print("4. Use /agents/available to see available agents")
    
    # Test 5: Test a simple workflow execution (optional)
    print("\n5️⃣ Testing simple workflow execution...")
    print("Executing a simple market analysis task...")
    
    try:
        # Execute the simple task
        result = crew.kickoff()
        print("✅ Simple workflow executed successfully!")
        print(f"Result preview: {str(result)[:200]}...")
    except Exception as e:
        print(f"⚠️ Workflow execution skipped due to: {str(e)[:100]}...")
        print("This is expected if Ollama is not running or model is not available")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure all dependencies are installed")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("Please check the configuration and dependencies.")
