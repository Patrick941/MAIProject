from openai import OpenAI
import datetime
import re
import os

class ResponseGenerator:
    def __init__(self, model='gpt-4-turbo'):
        self.model = model
        self.api_key = self.read_api_key()

    def read_api_key(self):
        file_path = os.path.dirname(os.path.abspath(__file__))
        api_key_path = os.path.join(file_path, '..', 'apiKey.txt')

        with open(api_key_path, 'r') as file:
            api_key = file.read().strip()
        return api_key

    def generate_response(self, query):
        client = OpenAI(api_key=self.api_key)
        response = client.chat.completions.create(model=self.model,
        messages=[
        {"role": "system", "content": "You are a software developer"},
        {"role": "user", "content": query}
        ],
        max_tokens=1000,
        temperature=0.7,
        n=1,
        stop=None)

        return response.choices[0].message.content