import matplotlib.pyplot as plt

# Data
features = ["Original", "Code Comparison", "Code Complexity Check", "Self Improvement"]
cognitive_complexity = [83, 83, 86, 87]
cyclomatic_complexity = [4, 4, 6, 6]
original_code_retry_count = [0.3, 0.3, 0.3, 0.2]
bug_insertion_retry_count = [1.5, 1.5, 1.5, 1]
code_similarity = [0.75, 0.7, 0.7, 0.72]

# Plotting
fig, axs = plt.subplots(5, 1, figsize=(10, 18), sharex=True)

axs[0].plot(features, cognitive_complexity, marker='o', label='Cognitive Complexity')
axs[0].set_ylabel('Cognitive Complexity')
axs[0].grid(True)

axs[1].plot(features, cyclomatic_complexity, marker='o', label='Cyclomatic Complexity')
axs[1].set_ylabel('Cyclomatic Complexity')
axs[1].grid(True)

axs[2].plot(features, original_code_retry_count, marker='o', label='Original Code Retry Count')
axs[2].set_ylabel('Original Code Retry Count')
axs[2].grid(True)

axs[3].plot(features, bug_insertion_retry_count, marker='o', label='Bug Insertion Retry Count')
axs[3].set_ylabel('Bug Insertion Retry Count')
axs[3].grid(True)

axs[4].plot(features, code_similarity, marker='o', label='Code Similarity')
axs[4].set_ylabel('Code Similarity')
axs[4].grid(True)

for ax in axs:
    ax.legend()
    ax.set_xticks(range(len(features)))
    ax.set_xticklabels(features, rotation=45)

plt.xlabel('Features')
plt.suptitle('Metrics by Feature')
plt.tight_layout(rect=[0, 0, 1, 0.96])

plt.savefig('Images/progress_plot.png')