import subprocess
import os
import ast
import random

class ASTBugInsertion:
    def __init__(self, file_path, bug_type, bug_count):
        self.file_path = file_path
        self.bug_type = bug_type
        self.bug_count = bug_count
        
    def insert_bug(self):
        with open(self.file_path, 'r') as file:
            content = file.read()
            tree = ast.parse(content)
            if self.bug_type == "Syntax":
                for i in range(self.bug_count):
                    rand_num = random.randint(0, 4)
                    if rand_num == 0:
                        for node in ast.walk(tree):
                            if isinstance(node, ast.FunctionDef):
                                node.name = "def"
                                break
                    elif rand_num == 1:
                        for node in ast.walk(tree):
                            if isinstance(node, ast.ClassDef):
                                node.name = "class"
                                break
                    elif rand_num == 2:
                        for node in ast.walk(tree):
                            if isinstance(node, ast.Import):
                                node.names[0].name = "!"
                                break
                    elif rand_num == 3:
                        for node in ast.walk(tree):
                            if isinstance(node, ast.Assign):
                                if hasattr(node.targets[0], 'id'):
                                    node.targets[0].id = "try"
                                    break
                    elif rand_num == 4:
                        for node in ast.walk(tree):
                            if isinstance(node, ast.If):
                                node.test = ast.Name(id="if", ctx=ast.Load())
                                break
                            
            if self.bug_type == "Semantic":
                for i in range(self.bug_count):
                    rand_num = random.randint(0, 5)
                    if rand_num == 0:
                        for node in ast.walk(tree):
                            if isinstance(node, ast.BinOp):
                                possible_ops = [ast.Add(), ast.Sub(), ast.Mult(), ast.Div(), ast.FloorDiv(), ast.Pow(), ast.Mod()]
                                current_op = type(node.op)
                                new_op = random.choice([op for op in possible_ops if type(op) != current_op])
                                node.op = new_op
                                break
                            elif rand_num == 1:
                                for node in ast.walk(tree):
                                    if isinstance(node, ast.Call):
                                        if node.args and random.choice([True, False]):
                                            node.args.pop(random.randrange(len(node.args)))
                                        else:
                                            node.args.append(ast.Constant(value="temp"))
                                        break
                            
                            
                
                    
                

            new_content = ast.unparse(tree)
            print("\033[92mOriginal content:\033[0m")
            print(content)
            print("\033[92mNew content:\033[0m")
            print(new_content)
        
        
def main():
    directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(directory, "temp.py")
    
    if not os.path.exists(file_path):
        print(f"File does not exist: {file_path}")
        return
    bug_type = "Semantic"
    bug_insertion = ASTBugInsertion(file_path, bug_type, 5)
    bug_insertion.insert_bug()
    
if __name__ == "__main__":
    main()    
