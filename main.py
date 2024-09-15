import Scripts.ollama_classes

def write_temp_script(language, topic, output_file_path):
    ollama_response_generator = Scripts.ollama_classes.OllamaResponseGenerator()
    response = ollama_response_generator.generate_response("Write a non-interactive program incorporating " + topic + " in " + language)
    start_index = response.find("```")
    end_index = response.rfind("```")
    extracted_text = response[start_index + 3:end_index]
    with open(output_file_path, 'w') as file:
        file.write(extracted_text)

def compile_script(output_file_path):
    import subprocess
    subprocess.run(["python", output_file_path])
    result = subprocess.run(["python", output_file_path])
    if result.returncode == 0:
        print("\033[92mScript executed successfully.\033[0m")  # Green color
    else:
        print("\033[91mScript execution failed.\033[0m")  # Red color
        
    
write_temp_script("Python", "loops", "output.py")
compile_script("output.py")
