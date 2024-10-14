import subprocess
import Scripts.ollama_classes as ollama_classes
import Scripts.openAI_classes as openAI_classes
import Scripts.code_generation as code_generation

class CodeRepair:
    def __init__(self, file_path, type, program_input, expected_output):
        self.file_path = file_path
        self.program_input = program_input
        self.expected_output = expected_output
        self.type = type

    def read_file(self):
        with open(self.file_path, 'r') as file:
            content = file.read()
            for counter in range(1, 5):
                output = self.test_script()
                if output is None:
                    break
                code_gen = code_generation.CodeGeneration("none", "none", self.file_path, self.type, "This code:\n\n" + content + "\nProduced the following output:\n\n"  + output + "\nThe expected output was:\n\n" + self.expected_output)
                code_gen.write_temp_script()
                
                
                
    def test_script(self):
        try:
            result = subprocess.run(['python', self.file_path], input=self.program_input, text=True, capture_output=True)
            output = result.stderr.strip() + result.stdout.strip()
            if output == self.expected_output:
                print("Test passed.")
                return None
            else:
                print(f"Test failed. Expected '{self.expected_output}', but got '{output}'.")
                return output
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while running the script: {e.stderr}")
            return e.stderr