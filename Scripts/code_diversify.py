import Scripts.code_generation as code_generation

class CodeDiversify:
    def __init__(self, problem_count, result_directory, model):
        self.result_directory = result_directory
        self.problem_count = problem_count
        self.model = model

    def diversify(self, problem_index, expected_output):
        for j in range(5):
            i = problem_index
            file_path = self.result_directory + "/output_" + str(i) + ".py"
            with open(file_path, 'r') as file:
                content = file.read()
            line_count = len(content.splitlines())
            code_gen = code_generation.CodeGeneration("NA", "NA", file_path, "ollama", self.model, self.result_directory, "Do some refactoring changes to this code (including or removing of functions or classes). Make sure the output doesn't change at all" + content)
            code_gen.write_temp_script()
            new_line_count = len(open(file_path, 'r').read().splitlines())
            if new_line_count > line_count * 1.3 or new_line_count < line_count * 0.7:
                with open(file_path, 'w') as file:
                    file.write(content)
                print("\033[91mDiversifying code likely failed, reverting change and returning error\033[0m")
                continue   
            result = code_gen.compile_script(True)
            if result != 1:
                std_result = result.stdout.strip()
                if std_result == expected_output:
                    return 0
                else:
                    with open(file_path, 'w') as file:
                        file.write(content)
                    print("\033[91mDiversifying code broke script, reverting change and trying again\033[0m")
                    continue
            else:
                continue
        print("\033[91mUnable to diversify code\033[0m")
        return 1