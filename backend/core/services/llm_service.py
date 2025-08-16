"""
LLM Service Module
==================

Centralized service for managing Ollama LLM interactions with configuration support.
Provides a clean interface for all AI model operations across the application.

Usage:
    from core.services.llm_service import LLMService
    
    llm = LLMService()
    response = llm.generate_response("Hello", agent_type="financial_advisor")
"""

import requests
import json
import logging
from typing import List, Dict, Any, Optional
import numpy as np
from config.app_config import app_config, get_agent_model, get_ollama_config

# Configure logging
logger = logging.getLogger(__name__)


class LLMService:
    """
    Centralized LLM service with configuration management
    
    This service provides a unified interface for all Ollama LLM operations,
    with support for agent-specific models and centralized configuration.
    """
    
    def __init__(self, agent_type: Optional[str] = None):
        """
        Initialize LLM Service
        
        Args:
            agent_type: Specific agent type for model selection (optional)
        """
        self.config = get_ollama_config()
        self.base_url = self.config.base_url.rstrip('/')
        self.agent_type = agent_type
        self.model_name = get_agent_model(agent_type) if agent_type else self.config.model_name
        
        logger.info(f"Initialized LLMService with model: {self.model_name}")
    
    def generate_response(self, 
                         prompt: str, 
                         system_prompt: Optional[str] = None,
                         temperature: Optional[float] = None,
                         max_tokens: Optional[int] = None,
                         agent_type: Optional[str] = None) -> str:
        """
        Generate a response using Ollama
        
        Args:
            prompt: The user's prompt/question
            system_prompt: Optional system prompt to set context
            temperature: Controls randomness (0.0 to 1.0)
            max_tokens: Maximum number of tokens to generate
            agent_type: Override agent type for model selection
            
        Returns:
            Generated response as string
        """
        # Use agent-specific model if provided
        model_name = self.model_name
        if agent_type:
            model_name = get_agent_model(agent_type)
        
        # Use configuration defaults if not specified
        temperature = temperature or self.config.temperature
        max_tokens = max_tokens or self.config.max_tokens
        
        url = f"{self.base_url}/api/generate"
        
        # Prepare the prompt with system message if provided
        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        
        payload = {
            "model": model_name,
            "prompt": full_prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens
            }
        }
        
        try:
            logger.debug(f"Sending request to Ollama with model: {model_name}")
            response = requests.post(url, json=payload, timeout=self.config.timeout)
            response.raise_for_status()
            
            response_data = response.json()
            generated_text = response_data.get('response', "I apologize, but I couldn't generate a proper response.")
            
            logger.debug(f"Received response of {len(generated_text)} characters")
            return generated_text
            
        except requests.exceptions.Timeout:
            logger.error(f"Ollama request timed out after {self.config.timeout} seconds")
            return "I apologize, but the request timed out. Please try again with a simpler query."
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error calling Ollama API: {str(e)}")
            return "I apologize, but I encountered an error processing your request."
    
    def generate_financial_advice(self, 
                                 query: str, 
                                 customer_data: Dict[str, Any],
                                 conversation_history: Optional[List[Dict[str, str]]] = None) -> str:
        """
        Generate financial advice based on customer data and query
        
        Args:
            query: User's financial question
            customer_data: Dictionary containing customer financial information
            conversation_history: Optional list of previous conversation messages
            
        Returns:
            Generated financial advice
        """
        system_prompt = """You are an expert financial advisor with years of experience. 
        Analyze the customer's complete financial profile and provide personalized, actionable financial advice. 
        Focus on being helpful while maintaining professionalism. Be specific and provide concrete steps."""
        
        # Prepare context with customer data
        context = f"""
        Customer Information:
        {json.dumps(customer_data, indent=2)}
        
        Previous Conversation:
        {json.dumps(conversation_history, indent=2) if conversation_history else 'No previous conversation'}
        
        User Query: {query}
        
        Please provide specific advice based on the above information.
        """
        
        return self.generate_response(
            prompt=context, 
            system_prompt=system_prompt,
            agent_type="financial_advisor"
        )
    
    def generate_news_analysis(self,
                              query: str,
                              news_data: Dict[str, Any],
                              customer_context: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate news analysis with market insights
        
        Args:
            query: User's news-related question
            news_data: Latest news and market sentiment data
            customer_context: Optional customer profile for personalization
            
        Returns:
            Generated news analysis
        """
        system_prompt = """You are a financial news intelligence specialist. 
        Analyze the provided market news and sentiment data to give personalized, contextual responses. 
        Focus on current market trends, relevant news impacts, and actionable insights.
        Keep responses professional but conversational."""
        
        context = f"""
        Market News and Sentiment:
        {json.dumps(news_data, indent=2)}
        
        Customer Context:
        {json.dumps(customer_context, indent=2) if customer_context else 'No customer context provided'}
        
        User Query: {query}
        """
        
        return self.generate_response(
            prompt=context,
            system_prompt=system_prompt,
            agent_type="news_intelligence"
        )
    
    def generate_credit_analysis(self,
                                query: str,
                                credit_data: Dict[str, Any],
                                customer_profile: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate credit analysis and recommendations
        
        Args:
            query: User's credit-related question
            credit_data: Customer's credit profile and analysis
            customer_profile: Optional additional customer information
            
        Returns:
            Generated credit analysis and recommendations
        """
        system_prompt = """You are a credit specialist and financial advisor with expertise in 
        credit cards, credit optimization, and debt management. Analyze the customer's credit profile 
        and provide personalized recommendations. Focus on specific, actionable advice."""
        
        context = f"""
        Credit Profile Analysis:
        {json.dumps(credit_data, indent=2)}
        
        Customer Profile:
        {json.dumps(customer_profile, indent=2) if customer_profile else 'No additional profile data'}
        
        User Query: {query}
        """
        
        return self.generate_response(
            prompt=context,
            system_prompt=system_prompt,
            agent_type="credit_specialist"
        )
    
    def generate_embeddings(self, text: str) -> List[float]:
        """
        Generate embeddings for text using Ollama
        
        Args:
            text: Input text to generate embeddings for
            
        Returns:
            List of floats representing the embedding vector
        """
        url = f"{self.base_url}/api/embeddings"
        
        payload = {
            "model": self.model_name,
            "prompt": text
        }
        
        try:
            response = requests.post(url, json=payload, timeout=self.config.timeout)
            response.raise_for_status()
            return response.json().get('embedding', [])
        except requests.exceptions.RequestException as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            return []
    
    def compute_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """
        Compute cosine similarity between two embeddings
        
        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector
            
        Returns:
            Cosine similarity score (0.0 to 1.0)
        """
        if not embedding1 or not embedding2:
            return 0.0
            
        embedding1 = np.array(embedding1)
        embedding2 = np.array(embedding2)
        
        return np.dot(embedding1, embedding2) / (
            np.linalg.norm(embedding1) * np.linalg.norm(embedding2)
        )
    
    def get_available_models(self) -> List[str]:
        """
        Get list of available Ollama models
        
        Returns:
            List of available model names
        """
        return self.config.available_models
    
    def switch_model(self, model_name: str, agent_type: Optional[str] = None) -> None:
        """
        Switch to a different Ollama model
        
        Args:
            model_name: Name of the model to switch to
            agent_type: Optional agent type to update specific agent model
        """
        if agent_type:
            app_config.ollama.agent_models[agent_type] = model_name
            if self.agent_type == agent_type:
                self.model_name = model_name
        else:
            self.model_name = model_name
            
        logger.info(f"Switched to model: {model_name}" + 
                   (f" for agent: {agent_type}" if agent_type else ""))
    
    def health_check(self) -> bool:
        """
        Check if Ollama service is available
        
        Returns:
            True if service is available, False otherwise
        """
        try:
            url = f"{self.base_url}/api/tags"
            response = requests.get(url, timeout=5)
            return response.status_code == 200
        except:
            return False


# Global LLM service instance
_llm_service = None


def get_llm_service(agent_type: Optional[str] = None) -> LLMService:
    """
    Get global LLM service instance
    
    Args:
        agent_type: Optional agent type for model selection
        
    Returns:
        LLMService instance
    """
    global _llm_service
    if _llm_service is None or (agent_type and _llm_service.agent_type != agent_type):
        _llm_service = LLMService(agent_type)
    return _llm_service


# Convenience functions for easy usage
def generate_response(prompt: str, agent_type: Optional[str] = None, **kwargs) -> str:
    """Quick response generation"""
    service = get_llm_service(agent_type)
    return service.generate_response(prompt, **kwargs)


def switch_global_model(model_name: str) -> None:
    """Switch global Ollama model"""
    global _llm_service
    app_config.ollama.model_name = model_name
    _llm_service = None  # Force recreation with new model


if __name__ == "__main__":
    # Example usage and testing
    print("=== LLM Service Configuration ===")
    service = LLMService()
    print(f"Base URL: {service.base_url}")
    print(f"Default Model: {service.model_name}")
    print(f"Available Models: {service.get_available_models()}")
    print(f"Health Check: {service.health_check()}")
    
    # Test different agent models
    for agent in ["news_intelligence", "financial_advisor", "credit_specialist"]:
        model = get_agent_model(agent)
        print(f"{agent}: {model}")
