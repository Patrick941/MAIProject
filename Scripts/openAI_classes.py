import openai
import datetime
import re

class ResponseGenerator:
    def __init__(self, model='gpt-4-turbo'):
        self.model = model
    
    def generate_response(self, query):
        response = openai.Completion.create(
            engine=self.model,
            prompt=query,
            max_tokens=100,
            temperature=0.7,
            n=1,
            stop=None
        )
        return response.choices[0].text.strip()