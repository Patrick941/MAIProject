import subprocess
import os
import Scripts.ollama_classes as ollama_classes
import Scripts.openAI_classes as openAI_classes

class LLMBugInsertion:
    def __init__(self, output_file_path):
        self.output_file_path = output_file_path

    
        