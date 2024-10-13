def write_temp_script(language, topic, output_file_path, type, prompt_override=None):
    if type == "ollama":
        response_generator = Scripts.ollama_classes.ResponseGenerator()
    elif type == "openAI":
        response_generator = Scripts.openAI_classes.ResponseGenerator()
    else:
        raise ValueError("Invalid type. Please specify 'ollama' or 'openAI'.")
    if prompt_override:
        response = response_generator.generate_response(prompt_override)
    else:
        response = response_generator.generate_response("Write a runnable non-interactive program incorporating " + topic + " in " + language)
    start_index = response.find("```")
    end_index = response.rfind("```")
    if start_index == end_index:
        end_index = len(response)
    extracted_text = response[start_index + 3:end_index]
    if extracted_text.startswith("Python\n") or extracted_text.startswith("python\n"):
        extracted_text = extracted_text[7:]
    with open(output_file_path, 'w') as file:
        file.write(extracted_text)

def compile_script(output_file_path, keepScripts):
    subprocess.run(["python", output_file_path])
    result = subprocess.run(["python", output_file_path])
    if result.returncode == 0:
        print("\033[92mScript executed successfully.\033[0m")  # Green color
        if not keepScripts:
            os.remove(output_file_path)
        else:
            if not os.path.exists("artifacts"):
                os.makedirs("artifacts")
            new_path = os.path.join("artifacts", os.path.basename(output_file_path))
            os.rename(output_file_path, new_path)
            print(f"\033[93mScript saved to {new_path}\033[0m")
    else:
        print("\033[91mScript execution failed.\033[0m")  # Red color