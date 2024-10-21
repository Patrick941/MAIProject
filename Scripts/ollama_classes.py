from langchain_ollama import OllamaLLM

class ResponseGenerator:
    def __init__(self, model):
        self.model = model
        self.llm = OllamaLLM(model=self.model)
    
    def generate_response(self, query):
        response = self.llm.invoke(query)
        return response
