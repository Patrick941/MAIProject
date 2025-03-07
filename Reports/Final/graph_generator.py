import csv
import numpy as np

import matplotlib.pyplot as plt

data_fields = ['Model', 'Time', 'Bug Type', 'Cognitive Complexity', 'Cyclomatic Complexity', 'Attempts Needed Code Generation', 'Attempts Needed Bug Insertion', 'Similarity Score']


data = [
    ['deepseek-r1:14b', 336, 'ast', 42.09500770126638, 8.25, 0.25, 0.0, 1.264786867842822],
    ['deepseek-r1:32b', 738, 'ast', 39.561042934660655, 9.75, 0.0, 0.0, 1.5353389955086514],
    ['qwen2.5:32b', 421, 'ast', 39.561042934660655, 9.75, 0.0, 0.0, 1.5353389955086514],
    ['mistral-small:latest', 250, 'ast', 54.62526813534531, 3.25, 1.25, 0.0, 1.7186293958428065],
    ['llama3.1:latest', 34, 'ast', 54.02561821697138, 3.0, 0.0, 0.0, 1.7857982596621405],
    ['deepseek-r1:14b', 1406, 'LLM', 54.02561821697138, 3.0, 0.0, 0.0, 1.7857982596621405],
    ['deepseek-r1:32b', 2498, 'LLM', 60.86216199882549, 7.25, 0.0, 1.0, 1.1279884324021796],
    ['qwen2.5:32b', 211, 'LLM', 60.86216199882549, 7.25, 0.0, 1.0, 1.1279884324021796],
    ['mistral-small:latest', 626, 'LLM', 64.06474075720814, 3.25, 1.0, 1.5, 1.7237238178905767],
    ['llama3.1:latest', 119, 'LLM', 66.32118077873075, 2.75, 0.25, 2.25, 1.339051358485823]
]


# Extract unique model and bug type combinations
combinations = list(set((row[0], row[2]) for row in data))

# Prepare data for plotting
times = []
attempts = []
inverse_similarity_scores = []
labels = []
for model, bug_type in combinations:
    for row in data:
        if row[0] == model and row[2] == bug_type:
            times.append(row[1])
            attempts.append(row[5] + row[6])  # Sum of 'Attempts Needed Code Generation' and 'Attempts Needed Bug Insertion'
            inverse_similarity_scores.append(1 / row[7])  # Inverse of 'Similarity Score'
            labels.append(f"{model}\n{bug_type}")
            break

# Sort the data by labels
sorted_data = sorted(zip(labels, times, attempts, inverse_similarity_scores), key=lambda x: x[0])
labels, times, attempts, inverse_similarity_scores = zip(*sorted_data)

# Scale attempts and inverse similarity scores to fit the time range
max_time = max(times)
max_attempts = max(attempts)
max_inverse_similarity_scores = max(inverse_similarity_scores)
scaled_attempts = [attempt * (max_time / max_attempts) for attempt in attempts]
scaled_inverse_similarity_scores = [score * (max_time / max_inverse_similarity_scores) for score in inverse_similarity_scores]

# Create bar chart
fig, ax = plt.subplots(figsize=(12, 6))

bar_width = 0.2
index = np.arange(len(labels))

bar1 = ax.bar(index, times, bar_width, label='Time', color='skyblue')
bar2 = ax.bar(index + bar_width, scaled_attempts, bar_width, label='Attempts (scaled)', color='lightgreen')
bar3 = ax.bar(index + 2 * bar_width, scaled_inverse_similarity_scores, bar_width, label='Diversity Score (scaled)', color='salmon')

ax.set_xlabel('Model and Bug Type')
ax.set_ylabel('Values')
ax.set_title('Model and Bug Insertion Comparison')
ax.set_xticks(index + 1.5 * bar_width)
ax.set_xticklabels(labels, rotation=45, ha='right')
ax.legend()

plt.tight_layout()
plt.savefig('Images/Model_Comparison.png')

# Prepare data for complexity scores plotting
cognitive_complexity = []
cyclomatic_complexity = []
labels = []
for model, bug_type in combinations:
    for row in data:
        if row[0] == model and row[2] == bug_type:
            cognitive_complexity.append(row[3])
            cyclomatic_complexity.append(row[4])
            labels.append(f"{model}\n{bug_type}")
            break

# Sort the data by labels
sorted_data = sorted(zip(labels, cognitive_complexity, cyclomatic_complexity), key=lambda x: x[0])
labels, cognitive_complexity, cyclomatic_complexity = zip(*sorted_data)

# Scale complexity scores to fit the range
max_cognitive_complexity = max(cognitive_complexity)
max_cyclomatic_complexity = max(cyclomatic_complexity)
scaled_cognitive_complexity = [score * (max_cognitive_complexity / max_cognitive_complexity) for score in cognitive_complexity]
scaled_cyclomatic_complexity = [score * (max_cognitive_complexity / max_cyclomatic_complexity) for score in cyclomatic_complexity]

# Create bar chart for complexity scores
fig, ax = plt.subplots(figsize=(12, 6))

bar_width = 0.35
index = np.arange(len(labels))

bar1 = ax.bar(index, scaled_cognitive_complexity, bar_width, label='Cognitive Complexity (scaled)', color='lightblue')
bar2 = ax.bar(index + bar_width, scaled_cyclomatic_complexity, bar_width, label='Cyclomatic Complexity (scaled)', color='lightcoral')

ax.set_xlabel('Model and Bug Type')
ax.set_ylabel('Complexity Scores (scaled)')
ax.set_title('Model and Bug Insertion Complexity Comparison')
ax.set_xticks(index + bar_width / 2)
ax.set_xticklabels(labels, rotation=45, ha='right')
ax.legend()

plt.tight_layout()
plt.savefig('Images/Complexity_Comparison.png')