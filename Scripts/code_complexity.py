import subprocess
import os
from radon.complexity import cc_visit
from radon.complexity import cc_visit, cc_rank
from radon.metrics import mi_visit
import Scripts.ollama_classes as ollama_classes
import Scripts.openAI_classes as openAI_classes

class codeComplexity:
    def __init__(self, file_path):
        self.file_path = file_path

    def get_complexity(self):
        try:
            with open(self.file_path, 'r') as file:
                code = file.read()
            cyclomatic_complexity = cc_visit(code)
            cognitive_complexity = mi_visit(code, multi=True)
            return {
                'cyclomatic_complexity': cyclomatic_complexity,
                'cognitive_complexity': cognitive_complexity
            }
        except ImportError:
            print("Please install the radon library to use this feature.")
        except Exception as e:
            print(f"An error occurred: {e}")