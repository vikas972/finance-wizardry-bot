from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict, Any
import json

class RAGPipeline:
    def __init__(self):
        # Initialize the embedding model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def generate_embedding(self, text: str) -> str:
        """Generate embedding for text and return as string"""
        embedding = self.model.encode(text)
        return json.dumps(embedding.tolist())
    
    def prepare_aa_data_text(self, data: Dict[str, Any]) -> str:
        """Convert AA data to text format for embedding"""
        text = f"""
        Account Summary: {json.dumps(data['account_summary'])}
        Spending Patterns: {json.dumps(data['spending_patterns'])}
        Assets: {json.dumps(data['assets'])}
        """
        return text
    
    def prepare_bureau_data_text(self, data: Dict[str, Any]) -> str:
        """Convert Bureau data to text format for embedding"""
        text = f"""
        Loan Details: {json.dumps(data['loan_details'])}
        Credit Score: {data['credit_score']}
        Repayment History: {json.dumps(data['repayment_history'])}
        """
        return text
    
    def prepare_itr_data_text(self, data: Dict[str, Any]) -> str:
        """Convert ITR data to text format for embedding"""
        text = f"""
        Tax Returns: {json.dumps(data['tax_returns'])}
        Taxable Income: {data['taxable_income']}
        Deductions: {json.dumps(data['deductions'])}
        """
        return text
    
    def compute_similarity(self, query_embedding: List[float], doc_embedding: List[float]) -> float:
        """Compute cosine similarity between query and document embeddings"""
        query_embedding = np.array(query_embedding)
        doc_embedding = np.array(doc_embedding)
        return np.dot(query_embedding, doc_embedding) / (
            np.linalg.norm(query_embedding) * np.linalg.norm(doc_embedding)
        )
    
    def retrieve_relevant_documents(self, query: str, documents: List[Dict[str, Any]], top_k: int = 3) -> List[Dict[str, Any]]:
        """Retrieve top-k most relevant documents for the query"""
        query_embedding = self.model.encode(query)
        
        # Calculate similarities
        similarities = []
        for doc in documents:
            doc_embedding = json.loads(doc['vector_embedding'])
            similarity = self.compute_similarity(query_embedding, doc_embedding)
            similarities.append((similarity, doc))
        
        # Sort by similarity and return top-k documents
        similarities.sort(reverse=True, key=lambda x: x[0])
        return [doc for _, doc in similarities[:top_k]] 