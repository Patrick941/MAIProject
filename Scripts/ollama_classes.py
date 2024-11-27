from langchain_ollama import OllamaLLM
import random

class ResponseGenerator:
    def __init__(self, model, temperature=None, max_tokens=None, top_p=None, top_k=None):
        self.model = model
        self.temperature = temperature if temperature is not None else random.uniform(0.1, 2.0)
        self.max_tokens = max_tokens if max_tokens is not None else random.randint(50, 1024)
        self.top_p = top_p if top_p is not None else random.uniform(0.1, 1.0)
        self.top_k = top_k if top_k is not None else random.randint(1, 50)
        
        self.llm = OllamaLLM(
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            top_p=self.top_p,
            top_k=self.top_k
        )
    
    def generate_response(self, query):
        response = self.llm.invoke(query)
        return response
