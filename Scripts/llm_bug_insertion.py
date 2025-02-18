import subprocess
import os
import Scripts.ollama_classes as ollama_classes
import Scripts.openAI_classes as openAI_classes
import Scripts.code_generation as code_generation

class LLMBugInsertion:
    def __init__(self, file_path, type, model, bug_description, results_directory):
        self.file_path = file_path
        self.model = model
        self.type = type
        self.bug = bug_description
        self.results_directory = results_directory

    def insert_bug(self):
        with open(self.file_path, 'r') as file:
            content = file.read()
            line_count = len(content.splitlines())
            if self.type == "ollama":
                code_gen = code_generation.CodeGeneration("NA", "NA", self.file_path, "ollama", self.model, self.results_directory, False, "Take this code:\n\n" + content + "\n\n Now, " + self.bug)
            elif self.type == "openAI":
                code_gen = code_generation.CodeGeneration("NA", "NA", self.file_path, "openAI", self.model, self.results_directory, False ,"Take this code:\n\n" + content + "\n\n Now, " + self.bug)
            code_gen.write_temp_script()
            new_content = open(self.file_path, 'r').read()
            new_line_count = len(new_content.splitlines())
            if new_line_count > line_count * 1.3 or new_line_count < line_count * 0.7:
                with open(self.file_path, 'w') as file:
                    file.write(content)
                print("Bug insertion likely failed, reverting change and returning error")
                return 1       
            return 0         
        
        