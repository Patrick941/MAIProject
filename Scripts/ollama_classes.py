from langchain_ollama import OllamaLLM

class ResponseGenerator:
    def __init__(self, model, temperature=1.2, max_tokens=256, top_p=0.8, top_k=None):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.top_p = top_p
        self.top_k = top_k
        
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
