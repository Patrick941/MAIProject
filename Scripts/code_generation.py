import subprocess
import os
import Scripts.ollama_classes as ollama_classes
import Scripts.openAI_classes as openAI_classes

class CodeGeneration:
    def __init__(self, language, topic, output_file_path, type, model, results_directory, debug=False, prompt_override=None, hyperparameters=None):
        self.language = language
        self.topic = topic
        self.output_file_path = output_file_path
        self.type = type
        self.prompt_override = prompt_override
        self.model = model
        self.results_directory = results_directory
        self.debug = debug
        self.hyperparameters = hyperparameters

    def write_temp_script(self):
        def extract_code_block(response):
            start_index = response.find("```")
            end_index = response.find("```", start_index + 3)
            if start_index == end_index:
                end_index = len(response)
            code = response[start_index + 3:end_index]
            if code.startswith(("Python\n", "python\n")):
                code = code[7:]
            return code

        def generate_input_file(code):
            input_prompt = f"Write the input file input.txt that will work with this code:\n{code}"
            input_response = response_generator.generate_response(input_prompt)
            extracted_input = extract_code_block(input_response)
            extracted_input = '\n'.join(extracted_input.split('\n')[1:])
            with open('input.txt', 'w') as file:
                file.write(extracted_input)
            return extracted_input

        if self.type == "ollama":
            args = {"model": self.model}
            if self.hyperparameters:
                args.update({
                    "temperature": self.hyperparameters[0],
                    "max_tokens": self.hyperparameters[1],
                    "top_p": self.hyperparameters[2],
                    "top_k": self.hyperparameters[3]
                })
            response_generator = ollama_classes.ResponseGenerator(**args)
        elif self.type == "openAI":
            response_generator = openAI_classes.ResponseGenerator()
        else:
            raise ValueError("Invalid type. Must be 'ollama' or 'openAI'.")

        prompt = self.prompt_override or (
            f"Write a runnable non-interactive program that takes the input file input.txt "
            f"incorporating {self.topic} in {self.language} that writes output to terminal"
        )
        
        current_code = extract_code_block(response_generator.generate_response(prompt))
        current_input = None if self.prompt_override else generate_input_file(current_code)

        max_retries = 3
        for attempt in range(max_retries + 1):
            check_prompt = (
                "Respond with just yes or no\n"
                f"Does this code:\n{current_code}\nFit this prompt: {prompt}"
            )
            if "yes" in response_generator.generate_response(check_prompt).lower():
                with open(self.output_file_path, 'w') as file:
                    file.write(current_code)
                return 0
            
            if attempt == max_retries:
                return 1
                
            improvement_prompt = (
                f"Improve this code to better fit: {prompt}\n"
                f"Previous code: {current_code}\n"
                "Provide only the improved code with no additional commentary."
            )
            current_code = extract_code_block(response_generator.generate_response(improvement_prompt))
            
            if not self.prompt_override:
                current_input = generate_input_file(current_code)

        return 1
        


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