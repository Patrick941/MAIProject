import textdistance

class CodeComparison:
    def __init__(self, problem_count):
        self.problem_count = problem_count

    def compare_code(self):
        results = [0] * self.problem_count
        for i in range(self.problem_count):
            results[i] = 0
            file1 = "artifacts/output_" + str(i) + ".py"
            for j in range(self.problem_count):
                if i == j:
                    continue
                file2 = "artifacts/output_" + str(j) + ".py"
                
                # Read files
                with open(file1, 'r') as f1, open(file2, 'r') as f2:
                    file1_text = f1.read()
                    file2_text = f2.read()
                
                # Use Levenshtein distance as a similarity score
                similarity_score = textdistance.levenshtein.normalized_similarity(file1_text, file2_text)
                
                # Add the similarity score to the result for file1
                results[i] += similarity_score

        return results

if __name__ == "__main__":
    problem_count = 10
    code_compare = CodeComparison(problem_count)
    results = code_compare.compare_code()
    print(results)
