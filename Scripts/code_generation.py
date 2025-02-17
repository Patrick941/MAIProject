import subprocess
import os
import Scripts.ollama_classes as ollama_classes
import Scripts.openAI_classes as openAI_classes

class CodeGeneration:
    def __init__(self, language, topic, output_file_path, type, model, results_directory, debug, prompt_override=None):
        self.language = language
        self.topic = topic
        self.output_file_path = output_file_path
        self.type = type
        self.prompt_override = prompt_override
        self.model = model
        self.results_directory = results_directory
        self.debug = debug

    def write_temp_script(self):
        if self.type == "ollama":
            response_generator = ollama_classes.ResponseGenerator(self.model)
        elif self.type == "openAI":
            response_generator = openAI_classes.ResponseGenerator()
        else:
            raise ValueError("Invalid type. Please specify 'ollama' or 'openAI'.")
        if self.prompt_override:
            prompt = self.prompt_override
            response = response_generator.generate_response(prompt)
        else:
            prompt = "Write a runnable non-interactive program incorporating " + self.topic + " in " + self.language
            response = response_generator.generate_response(prompt)
        start_index = response.find("```")
        end_index = response.find("```", start_index + 3)
        if start_index == end_index:
            end_index = len(response)
        extracted_text = response[start_index + 3:end_index]
        if extracted_text.startswith("Python\n") or extracted_text.startswith("python\n"):
            extracted_text = extracted_text[7:]
        
        # Self reflect
        # response = response_generator.generate_response("Does this code:\n" + extracted_text + "\nFit this prompt well: " + prompt)
        # if "yes" not in response.lower()[:10]:
        #     print("\033[91mCode failed on self reflection\033[0m")
        #     if self.debug:
        #         print(response)

        with open(self.output_file_path, 'w') as file:
            file.write(extracted_text)

    def compile_script(self, keepScripts):
        import sys
        try:
            result = subprocess.run([sys.executable, self.output_file_path], timeout=10, capture_output=True, text=True)
        except subprocess.TimeoutExpired:
            print("\033[91mScript execution timed out.\033[0m")
            return 1
        except Exception as e:
            result = subprocess.CompletedProcess(args=[sys.executable, self.output_file_path], returncode=1, stdout='', stderr=str(e))
            return result
        if result.returncode == 0:
            print("\033[92mScript executed successfully.\033[0m")
            if not keepScripts:
                os.remove(self.output_file_path)
            else:
                if not os.path.exists(self.results_directory):
                    os.makedirs(self.results_directory)
                new_path = os.path.join(self.results_directory, os.path.basename(self.output_file_path))
                os.rename(self.output_file_path, new_path)
                self.output_file_path = new_path
                print(f"\033[93mScript saved to {new_path}\033[0m")
        else:
            print("\033[91mScript execution failed.\033[0m")
            print(result.stderr)
        return result
    
    def update_path(self, new_path):
        self.output_file_path = new_path