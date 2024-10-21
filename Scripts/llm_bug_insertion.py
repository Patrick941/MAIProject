import subprocess
import os
import Scripts.ollama_classes as ollama_classes
import Scripts.openAI_classes as openAI_classes
import Scripts.code_generation as code_generation

class LLMBugInsertion:
    def __init__(self, file_path, type, model, bug_description):
        self.file_path = file_path
        self.model = model
        self.type = type
        self.bug = bug_description

    def insert_bug(self):
        with open(self.file_path, 'r') as file:
            content = file.read()
            code_generation = code_generation.CodeGeneration("NA", "NA", self.output_file_path, "ollama", self.model, "Take this code:\n\n" + content + "\n\n Now, " + self.bug)
            code_generation.write_temp_script()
        
        