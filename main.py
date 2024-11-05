import Scripts.code_repair as code_repair
import Scripts.code_generation as code_generation
import Scripts.code_complexity as code_complexity
import Scripts.llm_bug_insertion as llm_bug_insertion
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
        
model = "none"

def main():
    output_file_path = "output"
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", help="Specify the type: 'ollama' or 'openAI'")
    parser.add_argument("--amount", type=int, default=1, help="Specify the number of problems to generate")
    parser.add_argument("--save-scripts", type=bool, default=False, help="Save the generated scripts")
    parser.add_argument("--model", help="Specify the model to use", default="llama3.1")
    args = parser.parse_args()

    type = args.type
    problemCount = args.amount
    keepScripts = args.save_scripts
    global model
    model = args.model
    results = {}
    output_log = open("output.log", "w")
    output_csv = open("output.csv", "w")
    output_csv.write("Problem Number,Cognitive Complexity,Cyclomatic complexity,Attempts needed for original code,Attempts needed for bug insertion\n")

    for index in range(problemCount):
        successful_script = False
        for attempt in range(5):
            if successful_script:
                results[index] = "success"
                break
            try:
                print("\033[93mGenerating problem " + str(index) + "...\033[0m")
                local_output_file_path = output_file_path + "_" + str(index) + ".py"
                code_gen = code_generation.CodeGeneration("Python", "High Dimensionality Arrays", local_output_file_path, type, model)
                code_gen.write_temp_script()
                script_result = code_gen.compile_script(keepScripts)
                if script_result.returncode != 0:
                    print("\033[91mScript failed to compile. Trying again...\033[0m")
                    continue
                expected_output = script_result.stdout.strip()
                print("\033[92mOriginal working script compiled correctly\033[0m")
                local_output_file_path = os.path.join("artifacts", os.path.basename(local_output_file_path))
                code_gen.update_path(local_output_file_path)
                successful_script = True
                
                successful_bug_insert = False
                for bug_attempt in range(6):
                    if successful_bug_insert:
                        break
                    try:                        
                        bug_insert = llm_bug_insertion.LLMBugInsertion(local_output_file_path, type, model, "add a bug in the indexing of the array")
                        if bug_insert.insert_bug() != 0: continue
                        script_result = code_gen.compile_script(keepScripts)
                        if script_result == 0:
                            if script_result.stdout.strip() == expected_output:    
                                print("\033[91mFailed to insert bug\033[0m")
                                continue
                            else:
                                print("\033[92mBug inserted successfully\033[0m")
                                successful_bug_insert = True
                        else:
                            print("\033[92mBug inserted successfully\033[0m")
                            print("Received output: " + script_result.stdout.strip() + "\nExpected output: " + expected_output)
                            output_log.write("Problem: " + str(index) + "\nReceived output: " + script_result.stdout.strip() + "\nExpected output: " + expected_output)
                            code_complex = code_complexity.codeComplexity(local_output_file_path)
                            complexity_results = code_complex.get_complexity()
                            cognitive_complexity = complexity_results['cognitive_complexity']
                            cyclomatic_complexity = complexity_results['cyclomatic_complexity'][0].complexity
                            output_csv.write(f"{index},{cognitive_complexity},{cyclomatic_complexity},{attempt},{bug_attempt}\n")
                            successful_bug_insert = True
                    except Exception as e:
                        print("\033[91mThere was an error inserting the bug. Trying again...\033[0m")
                        print(e)
                        continue
                if not successful_bug_insert:
                    successful_script = False                
                
                
            except Exception as e:
                print("\033[91mThere was an error with the generated code. Trying again...\033[0m")
                print(e)
                subprocess.run(["ollama", "stop", model])
                continue
    
    for key, value in results.items():
        print(f"Problem {key}: {value}")

    output_log.close()
    output_csv.close()
    if not os.path.exists("artifacts"):
        os.makedirs("artifacts")
    os.rename("output.log", os.path.join("artifacts", "output.log"))
    os.rename("output.csv", os.path.join("artifacts", "output.csv"))

if __name__ == "__main__":
    try:
        main()
        if model == "ollama":
            subprocess.run(["ollama", "stop", model])
        print("\033[92mScript execution completed successfully.\033[0m")
        for file in os.listdir():
            if file.startswith("output"):
                os.remove(file)
    except KeyboardInterrupt:
        if model == "ollama":
            subprocess.run(["ollama", "stop", model])
        for file in os.listdir():
            if file.startswith("output"):
                os.remove(file)
        print("\033[91mScript execution interrupted by user.\033[0m")