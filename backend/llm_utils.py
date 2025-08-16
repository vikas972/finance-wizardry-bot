import requests
import json
from typing import List, Dict, Any, Optional
import numpy as np

class OllamaLLM:
    def __init__(self, model_name: str = "deepseek-r1:1.5b", base_url: str = "http://localhost:11434"):
        """Initialize Ollama LLM client
        
        Args:
            model_name: Name of the Ollama model to use (default: deepseek-coder:1.5b)
            base_url: Base URL for Ollama API (default: http://localhost:11434)
        """
        self.model_name = model_name
        self.base_url = base_url.rstrip('/')
        
    def generate_response(self, 
                         prompt: str, 
                         system_prompt: Optional[str] = None,
                         temperature: float = 0.7,
                         max_tokens: int = 500) -> str:
        """Generate a response using Ollama
        
        Args:
            prompt: The user's prompt/question
            system_prompt: Optional system prompt to set context
            temperature: Controls randomness (0.0 to 1.0)
            max_tokens: Maximum number of tokens to generate
            
        Returns:
            Generated response as string
        """
        url = f"{self.base_url}/api/generate"
        
        # Prepare the prompt with system message if provided
        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        
        payload = {
            "model": self.model_name,
            "prompt": full_prompt,
            "stream": False
        }
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()  # Raise an error for bad status codes
            
            # Debug information
            print(f"Ollama API Response Status: {response.status_code}")
            print(f"Ollama API Response: {response.text[:500]}...")  # Print first 500 chars
            
            response_data = response.json()
            return response_data.get('response', "I apologize, but I couldn't generate a proper response.")
            
        except requests.exceptions.RequestException as e:
            print(f"Error calling Ollama API: {str(e)}")
            print(f"Response content: {getattr(e.response, 'text', 'No response content')}")
            return "I apologize, but I encountered an error processing your request."
            
    def generate_embeddings(self, text: str) -> List[float]:
        """Generate embeddings for text using Ollama
        
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
            response = requests.post(url, json=payload)
            response.raise_for_status()
            return response.json().get('embedding', [])
        except requests.exceptions.RequestException as e:
            print(f"Error generating embeddings: {str(e)}")
            return []
            
    def compute_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """Compute cosine similarity between two embeddings"""
        if not embedding1 or not embedding2:
            return 0.0
            
        embedding1 = np.array(embedding1)
        embedding2 = np.array(embedding2)
        
        return np.dot(embedding1, embedding2) / (
            np.linalg.norm(embedding1) * np.linalg.norm(embedding2)
        )

    def get_financial_advice(self, 
                           query: str, 
                           customer_data: Dict[str, Any],
                           conversation_history: Optional[List[Dict[str, str]]] = None) -> str:
        """Generate financial advice based on customer data and query
        
        Args:
            query: User's question
            customer_data: Dictionary containing customer financial information
            conversation_history: Optional list of previous conversation messages
            
        Returns:
            Generated financial advice
        """
        system_prompt = """You are an AI financial advisor. Your role is to provide clear, 
        accurate, and personalized financial advice based on the customer's data and query. 
        Focus on being helpful while maintaining professionalism."""
        
        # Prepare context with customer data
        context = f"""
        Customer Information:
        {json.dumps(customer_data, indent=2)}
        
        Previous Conversation:
        {json.dumps(conversation_history, indent=2) if conversation_history else 'No previous conversation'}
        
        User Query: {query}
        
        Please provide specific advice based on the above information.
        """
        
        return self.generate_response(context, system_prompt=system_prompt) 