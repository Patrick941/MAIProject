from langchain.llms import Ollama
import datetime
import re

class OllamaResponseGenerator:
    def __init__(self, model='llama3'):
        self.model = model
        self.llm = Ollama(model=self.model)
    
    def generate_response(self, query):
        response = self.llm.predict(query)
        return response
