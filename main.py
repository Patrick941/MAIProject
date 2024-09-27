import Scripts.ollama_classes
import Scripts.openAI_classes
import subprocess
import os
import ast
import random
import argparse

def write_temp_script(language, topic, output_file_path, type):
    if type == "ollama":
        response_generator = Scripts.ollama_classes.ResponseGenerator()
    elif type == "openAI":
        response_generator = Scripts.openAI_classes.ResponseGenerator()
    else:
        raise ValueError("Invalid type. Please specify 'ollama' or 'openAI'.")
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

def compile_script(output_file_path):
    subprocess.run(["python", output_file_path])
    result = subprocess.run(["python", output_file_path])
    if result.returncode == 0:
        print("\033[92mScript executed successfully.\033[0m")  # Green color
        os.remove(output_file_path)
    else:
        print("\033[91mScript execution failed.\033[0m")  # Red color
        
def analyse_script(output_file_path):
    with open(output_file_path, "r") as temp_script:
        code = temp_script.read()
        tree = ast.parse(code)
        return tree
    
def insert_bug(tree, output_file_path):
    nodes = [node for node in ast.walk(tree) if isinstance(node, ast.Expr) and isinstance(node.value, ast.Num)]
    if not nodes:
        print("\033[91mNo suitable node found to insert a bug.\033[0m")
        return
    node = random.choice(nodes)
    node.value = ast.BinOp(left=node.value, op=ast.Add(), right=ast.Constant(value=1))
    new_script = ast.unparse(tree)
    original_script = open(output_file_path, "r").read()
    if new_script == original_script:
        print("\033[92mNo bug inserted.\033[0m")
    print("\033[92mOriginal script:\n\033[0m" + original_script)
    print("\033[91mNew script:\n\033[0m" + new_script)
        
    

output_file_path = "output.py"
parser = argparse.ArgumentParser()
parser.add_argument("--type", help="Specify the type: 'ollama' or 'openAI'")
parser.add_argument("--amount", type=int, default=1, help="Specify the number of problems to generate")
args = parser.parse_args()

type = args.type
problemCount = args.amount
for problem, index in enumerate(range(problemCount)):
    for attempt in range(3):
        try:
            print("\033[93mGenerating problem " + str(index) + "...\033[0m")
            local_output_file_path = output_file_path + "_" + str(index) + ".py"
            write_temp_script("Python", "loops", local_output_file_path, type)
            tree = analyse_script(local_output_file_path)
            insert_bug(tree, local_output_file_path)
            compile_script(local_output_file_path)
        except:
            print("\033[91mThere was an error with the generated code. Trying again...\033[0m")
            continue