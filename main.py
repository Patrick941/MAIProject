import Scripts.code_repair as code_repair
import Scripts.code_generation as code_generation
import subprocess
import os
import ast
import random
import argparse
        
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
parser.add_argument("--save-scripts", type=bool, default=False, help="Save the generated scripts")
args = parser.parse_args()

type = args.type
problemCount = args.amount
keepScripts = args.save_scripts

for problem, index in enumerate(range(problemCount)):
    for attempt in range(3):
        try:
            print("\033[93mGenerating problem " + str(index) + "...\033[0m")
            local_output_file_path = output_file_path + "_" + str(index) + ".py"
            code_generation = code_generation.CodeGeneration("Python", "loops", local_output_file_path, type)
            code_generation.write_temp_script()
            code_generation.compile_script()
        except:
            print("\033[91mThere was an error with the generated code. Trying again...\033[0m")
            continue