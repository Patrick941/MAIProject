import Scripts.code_repair as code_repair
import Scripts.code_generation as code_generation
import Scripts.code_complexity as code_complexity
import Scripts.llm_bug_insertion as llm_bug_insertion
import Scripts.code_comparison as code_comparison
import Scripts.code_diversify as code_diversify
import Scripts.ast_bug_insertion as ast_bug_insertion
import subprocess
import os
import ast
import random
import argparse
import csv
import sys

class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def writelines(self, datas):
       self.stream.writelines(datas)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)
        
def analyse_script(output_file_path):
    with open(output_file_path, "r") as temp_script:
        code = temp_script.read()
        tree = ast.parse(code)
        return tree
        
model = "none"

def main():
    output_file_path = "output"
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", help="Specify the type: 'ollama' or 'openAI'")
    parser.add_argument("--amount", type=int, default=1, help="Specify the number of problems to generate")
    parser.add_argument("--save-scripts", type=bool, default=False, help="Save the generated scripts")
    parser.add_argument("--model", help="Specify the model to use", default="llama3.1")
    parser.add_argument("--results-directory", type=str)
    parser.add_argument("--prompt-override", type=str)
    parser.add_argument("--ast-bug", type=bool, default=False)
    parser.add_argument("--bug-override", type=str)
    parser.add_argument("--skip-generation", type=bool, default=False)
    parser.add_argument("--test-case-count", type=int, default=1)
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()
    
    if args.ast_bug:
        print("\033[93mAST bug insertion enabled\033[0m")

    type = args.type
    debug = args.debug
    language = "Python"
    problemCount = args.amount
    keepScripts = args.save_scripts
    global model
    model = args.model
    results = {}
    output_log = open("output.log", "w")
    output_csv = open("output.csv", "w")
    
    if args.results_directory is not None:
        results_directory = args.results_directory
    else:
        results_directory = "artifacts"
    results_dict = {
        "Problem Number": [],
        "Cognitive Complexity": [],
        "Cyclomatic Complexity": [],
        "Attempts needed for original code": [],
        "Attempts needed for bug insertion": [],
        "Similarity": []
    }

    bug_output = []
    code_diverse = code_diversify.CodeDiversify(problemCount, results_directory, model)
    if not args.skip_generation:
        for index in range(problemCount):
            successful_script = False
            for attempt in range(5):
                if successful_script:
                    results[index] = "success"
                    break
                try:
                    print("\033[93mGenerating problem " + str(index) + "...\033[0m")
                    local_output_file_path = output_file_path + "_" + str(index) + ".py"
                    if args.prompt_override is None:
                        code_gen = code_generation.CodeGeneration(language, "Djikstra's Algorithm", local_output_file_path, type, model, results_directory, debug)
                    else:
                        code_gen = code_generation.CodeGeneration(language, args.prompt_override, local_output_file_path, type, model, results_directory)
                    return_code = code_gen.write_temp_script()
                    if return_code == 1:
                        print("\033[91mSelf reflection caused retry\033[0m")
                        continue
                    script_result = code_gen.compile_script(keepScripts)
                    if script_result.returncode != 0:
                        print("\033[91mFailed to generate code. Trying again...\033[0m")

                        continue
                    expected_output = script_result.stdout.strip()
                    print("\033[92mOriginal working script compiled correctly\033[0m")
                    local_output_file_path = os.path.join(results_directory, os.path.basename(local_output_file_path))
                    code_gen.update_path(local_output_file_path)
                    successful_script = True

                    if args.ast_bug:
                        bug_insert = ast_bug_insertion.ASTBugInsertion(local_output_file_path, "Semantic", 4)
                        bug_insert.insert_bug()
                        code_complex = code_complexity.codeComplexity(local_output_file_path)
                        complexity_results = code_complex.get_complexity()
                        cognitive_complexity = complexity_results['cognitive_complexity']
                        cyclomatic_complexity = complexity_results['cyclomatic_complexity'][0].complexity
                        
                        successful_bug_insert = True
                        results_dict["Problem Number"].append(index)
                        results_dict["Cognitive Complexity"].append(cognitive_complexity)
                        results_dict["Cyclomatic Complexity"].append(cyclomatic_complexity)
                        results_dict["Attempts needed for original code"].append(attempt)
                        results_dict["Attempts needed for bug insertion"].append(0)
                        
                    else:
                        successful_bug_insert = False
                        for bug_attempt in range(6):
                            if successful_bug_insert:
                                break
                            try:     
                                if args.bug_override is None:                 
                                    bug_insert = llm_bug_insertion.LLMBugInsertion(local_output_file_path, type, model, "add a bug in the djikstra algorithm implementation", results_directory)
                                else:
                                    bug_insert = llm_bug_insertion.LLMBugInsertion(local_output_file_path, type, args.bug_override, results_directory)
                                if bug_insert.insert_bug() != 0: continue
                                script_result = code_gen.compile_script(keepScripts)
                                if script_result == 0:
                                    if script_result.stdout.strip() == expected_output:    
                                        print("\033[91mFailed to insert bug\033[0m")
                                        continue
                                    else:
                                        print("\033[92mBug inserted successfully\033[0m")
                                        successful_bug_insert = True
                                elif script_result == 1:
                                    print("\033[91mScript execution timed out. Trying again...\033[0m")
                                    continue
                                else:
                                    print("\033[92mBug inserted successfully\033[0m")
                                    print("Received output: " + script_result.stdout.strip() + "\nExpected output: " + expected_output)
                                    bug_result = script_result.stdout.strip()
                                    output_log.write("Problem: " + str(index) + "\nReceived output: " +  bug_result + "\nExpected output: " + expected_output)
                                    bug_output.append(bug_result)
                                    
                                    code_complex = code_complexity.codeComplexity(local_output_file_path)
                                    complexity_results = code_complex.get_complexity()
                                    cognitive_complexity = complexity_results['cognitive_complexity']
                                    cyclomatic_complexity = complexity_results['cyclomatic_complexity'][0].complexity
                                    results_dict["Problem Number"].append(index)
                                    results_dict["Cognitive Complexity"].append(cognitive_complexity)
                                    results_dict["Cyclomatic Complexity"].append(cyclomatic_complexity)
                                    results_dict["Attempts needed for original code"].append(attempt)
                                    results_dict["Attempts needed for bug insertion"].append(bug_attempt)
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
            if successful_script == False:
                if not os.path.exists(results_directory):
                    os.makedirs(results_directory)
                failed_output_file_path = os.path.join(results_directory, os.path.basename(local_output_file_path).replace(".py", "_failed.py"))
                os.rename(local_output_file_path, failed_output_file_path)
    else:
        for i in range(problemCount):
            file_path = results_directory + "/output_" + str(i) + ".py"
            result = subprocess.run(["python", file_path], timeout=10, capture_output=True, text=True, errors='replace')
            bug_output.append(result.stdout.strip())

    similarity_threshold = 3

    code_compare = code_comparison.CodeComparison(problemCount, results_directory)
    comparison_results = code_compare.compare_code()
    for i in range(problemCount):
        if comparison_results[i] >  similarity_threshold and random.randint(1, 3) == 1:
            print(f"\033[94mProblem {i} is too similar to another problem (Similarity: {comparison_results[i]}, Threshold: {similarity_threshold}). Diversifying code...\033[0m")
            if code_diverse.diversify(i, bug_output[i]) ==  0: continue
        results_dict["Similarity"].append(comparison_results[i])
    comparison_results = code_compare.compare_code()
    
    with open("output.csv", "w", newline='') as csvfile:
        fieldnames = results_dict.keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerows([dict(zip(fieldnames, row)) for row in zip(*results_dict.values())])
        
        averages = {key: sum(value) / len(value) if value else 0 for key, value in results_dict.items() if key != "Problem Number"}
        averages["Problem Number"] = "Average"
        writer.writerow(averages)
    
    for key, value in results.items():
        print(f"Problem {key}: {value}")

    output_log.close()
    output_csv.close()
    if not os.path.exists(results_directory):
        os.makedirs(results_directory)
    os.rename("output.log", os.path.join(results_directory, "output.log"))
    os.rename("output.csv", os.path.join(results_directory, "output.csv"))

if __name__ == "__main__":
    try:
        sys.stdout = Unbuffered(sys.stdout)
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