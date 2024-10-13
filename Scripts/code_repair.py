import subprocess
import ollama_classes
import openAI_classes
import code_generation

class code_repair:
    def __init__(self, file_path, type, program_input, expected_output):
        self.file_path = file_path
        self.program_input = program_input
        self.expected_output = expected_output
        if type == "ollama":
            self.response_generator = Scripts.ollama_classes.ResponseGenerator()
        elif type == "openAI":
            self.response_generator = Scripts.openAI_classes.ResponseGenerator()
        else:
            raise ValueError("Invalid type. Please specify 'ollama' or 'openAI'.")

    def read_file(self):
        with open(self.file_path, 'r') as file:
            content = file.read()
            for counter in range(1, 5):
                output = self.test_script()
                if output is None:
                    break
                write_temp_script("none", "none", self.file_path, type, "This code:\n\n" + content + "\nProduced the following output:\n\n"  + output + "\nThe expected output was:\n\n" + self.expected_output)
                
                
                
    def test_script(self):
        try:
            result = subprocess.run(['python', self.file_path],input=self.program_input,text=True,capture_output=True,check=True)
            output = result.stdout.strip()
            if output == self.expected_output:
                print("Test passed.")
                return None
            else:
                print(f"Test failed. Expected '{self.expected_output}', but got '{output}'.")
                return output
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while running the script: {e}")
            return e
        
code_repair("test.py", "ollama", "", "Hello, World!").read_file()
            