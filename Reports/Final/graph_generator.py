import csv
import numpy as np
import matplotlib.pyplot as plt

def generate_graphs(data, category):
    combinations = list(set((row[0], row[2]) for row in data))

    times = []
    attempts = []
    labels = []
    for model, bug_type in combinations:
        for row in data:
            if row[0] == model and row[2] == bug_type:
                times.append(row[1])
                attempts.append(row[5] + row[6])
                labels.append(f"{model}\n{bug_type}")
                break

    sorted_data = sorted(zip(labels, times, attempts), key=lambda x: x[0])
    labels, times, attempts = zip(*sorted_data)

    fig, ax1 = plt.subplots(figsize=(14, 8))

    bar_width = 0.3
    index = np.arange(len(labels))

    ax1.bar(index, times, bar_width, label='Time (s)', color='skyblue')
    ax1.set_xlabel('Model and Bug Type')
    ax1.set_ylabel('Time (s)')
    ax1.tick_params(axis='y')

    ax2 = ax1.twinx()
    ax2.bar(index + bar_width, attempts, bar_width, label='Attempts', color='lightgreen')
    ax2.set_ylabel('Attempts')
    ax2.tick_params(axis='y')

    ax1.set_xticks(index + bar_width / 2)
    ax1.set_xticklabels(labels, rotation=45, ha='right')

    fig.tight_layout()
    plt.title('Model and Bug Insertion Comparison', pad=20)
    plt.savefig(f'Images/Model_Comparison_{category}.png')

    cognitive_complexity = []
    cyclomatic_complexity = []
    inverse_similarity_scores = []
    labels = []
    for model, bug_type in combinations:
        for row in data:
            if row[0] == model and row[2] == bug_type:
                cognitive_complexity.append(row[3])
                cyclomatic_complexity.append(row[4])
                inverse_similarity_scores.append(1 / row[7])
                labels.append(f"{model}\n{bug_type}")
                break

    sorted_data = sorted(zip(labels, cognitive_complexity, cyclomatic_complexity, inverse_similarity_scores), key=lambda x: x[0])
    labels, cognitive_complexity, cyclomatic_complexity, inverse_similarity_scores = zip(*sorted_data)

    fig, ax1 = plt.subplots(figsize=(14, 8))

    bar_width = 0.2
    index = np.arange(len(labels))

    ax1.bar(index, cognitive_complexity, bar_width, label='Cognitive Complexity', color='lightblue')
    ax1.set_xlabel('Model and Bug Type')
    ax1.set_ylabel('Cognitive Complexity')
    ax1.tick_params(axis='y')

    ax2 = ax1.twinx()
    ax2.bar(index + bar_width, cyclomatic_complexity, bar_width, label='Cyclomatic Complexity', color='lightcoral')
    ax2.set_ylabel('Cyclomatic Complexity')
    ax2.tick_params(axis='y')

    ax3 = ax1.twinx()
    ax3.spines['right'].set_position(('outward', 60))
    ax3.bar(index + 2 * bar_width, inverse_similarity_scores, bar_width, label='Diversity Score', color='lightgreen')
    ax3.set_ylabel('Diversity Score')
    ax3.tick_params(axis='y')

    ax1.set_xticks(index + bar_width)
    ax1.set_xticklabels(labels, rotation=45, ha='right')

    fig.tight_layout()
    plt.title('Model and Bug Insertion Complexity and Diversity Comparison', pad=20)
    plt.savefig(f'Images/Complexity_Comparison_{category}.png')
    
data_fields = ['Model', 'Time', 'Bug Type', 'Cognitive Complexity', 'Cyclomatic Complexity', 'Attempts Needed Code Generation', 'Attempts Needed Bug Insertion', 'Similarity Score']


fibbonaci_data = [
    ['deepseek-r1:14b', 336, 'ast', 42.09500770126638, 8.25, 0.25, 0.0, 1.264786867842822],
    ['deepseek-r1:32b', 738, 'ast', 39.561042934660655, 9.75, 0.0, 0.0, 1.5353389955086514],
    ['qwen2.5:32b', 421, 'ast', 39.561042934660655, 9.75, 0.0, 0.0, 1.5353389955086514],
    ['mistral-small:latest', 250, 'ast', 54.62526813534531, 3.25, 1.25, 0.0, 1.7186293958428065],
    ['llama3.1:latest', 34, 'ast', 54.02561821697138, 3.0, 0.0, 0.0, 1.7857982596621405],
    ['deepseek-r1:14b', 1406, 'LLM', 54.02561821697138, 3.0, 0.0, 0.0, 1.7857982596621405],
    ['deepseek-r1:32b', 2498, 'LLM', 60.86216199882549, 7.25, 0.0, 1.0, 1.1279884324021796],
    ['qwen2.5:32b', 1211, 'LLM', 60.86216199882549, 7.25, 0.0, 1.0, 1.1279884324021796],
    ['mistral-small:latest', 626, 'LLM', 64.06474075720814, 3.25, 1.0, 1.5, 1.7237238178905767],
    ['llama3.1:latest', 119, 'LLM', 66.32118077873075, 2.75, 0.25, 2.25, 1.339051358485823]
]

generate_graphs(fibbonaci_data, 'Fibbonaci')

arrays_data = [
    ['deepseek-r1:14b', 207, 'ast', 63.12071461504161, 6.0, 0.0, 0.0, 1.4441701441350696],
    ['deepseek-r1:32b', 396, 'ast', 66.94739669130495, 4.0, 0.0, 0.0, 1.4600899835034047],
    ['qwen2.5:32b', 131, 'ast', 68.23968510820585, 3.0, 0.0, 0.0, 1.3688708240608463],
    ['mistral-small:latest', 90, 'ast', 62.08678486455445, 2.3333333333333335, 0.0, 0.0, 1.1875465723403238],
    ['llama3.1:latest', 32, 'ast', 62.08678486455445, 2.3333333333333335, 0.0, 0.0, 1.287885175059529],
    ['deepseek-r1:14b', 4573, 'LLM', 62.08678486455445, 2.3333333333333335, 0.0, 0.0, 1.287885175059529],
    ['deepseek-r1:32b', 1449, 'LLM', 81.38652337639516, 5.75, 0.5, 0.0, 1.1883703446227445],
    ['qwen2.5:32b', 204, 'LLM', 95.6530252142819, 5.25, 0.0, 0.0, 1.6421644073678494],
    ['mistral-small:latest', 226, 'LLM', 89.09474424821052, 2.25, 0.0, 1.25, 1.0869497652683084],
    ['llama3.1:latest', 51, 'LLM', 78.39134688369425, 3.0, 0.0, 0.0, 1.6625950552302293]
]

djikstra_data = [
    ['deepseek-r1:14b', 2169, 'ast', 52.90784672532485, 7, 0.0, 0.0, 0.8236346346234523],
    ['deepseek-r1:32b', 1658, 'ast', 47.77039441632663, 12.0, 0.75, 0.0, 0.697969831521052],
    ['qwen2.5:32b', 246, 'ast', 50.23656721787658, 6.0, 0.5, 0.0, 1.178323574574745],
    ['mistral-small:latest', 606, 'ast', 56.366682052612305, 6.0, 0.5, 0.0, 0.972234634634574],
    ['llama3.1:latest', 62, 'ast', 50.86604877417025, 6.0, 0.5, 0.0, 1.593373966489731],
    ['deepseek-r1:14b', 3555, 'LLM', 72.44380456483157, 8.666666666666666, 2.3333333333333335, 1.3333333333333333, 0.556072139682153],
    ['deepseek-r1:32b', 4593, 'LLM', 70.3666820526123, 8.0, 2, 2, 2.134573463463452],
    ['qwen2.5:32b', 1256, 'LLM', 64.6787348563478, 7.0, 1.5, 3.5, 1.4634557346346],
    ['mistral-small:latest', 1062, 'LLM', 63.7457342363463, 7.5, 2.0, 4.0, 0.7346235234634],
    ['llama3.1:latest', 125, 'LLM', 61.2786897964123, 7.0, 1.5, 4.5, 2.2531123756434]
]

linked_lists_data = [
    ['deepseek-r1:14b', 1188, 'ast', 58.01428067018303, 6.5, 0.0, 0.0, 1.3839023893792609],
    ['deepseek-r1:32b', 1027, 'ast', 57.35899555381579, 8.0, 0.375, 0.0, 1.329030407512228],
    ['qwen2.5:32b', 188, 'ast', 59.23812616304122, 4.5, 0.25, 0.0, 1.5235971993177956],
    ['mistral-small:latest', 348, 'ast', 59.22673345858338, 4.166666666666667, 0.25, 0.0, 1.3298906034874349],
    ['llama3.1:latest', 47, 'ast', 56.47641681936245, 4.166666666666667, 0.25, 0.0, 1.69062957027463],
    ['deepseek-r1:14b', 4064, 'LLM', 67.26529471569286, 5.5, 1.1666666666666667, 0.6666666666666666, 1.1716076573708412],
    ['deepseek-r1:32b', 3021, 'LLM', 75.87660271450373, 6.875, 1.25, 1.0, 1.911471904043098],
    ['qwen2.5:32b', 730, 'LLM', 80.16588003531485, 6.125, 1.0, 1.75, 1.8028090909712247],
    ['mistral-small:latest', 644, 'LLM', 76.42023924242841, 4.875, 1.0, 2.5, 1.1607866449513362],
    ['llama3.1:latest', 88, 'LLM', 69.83501834005327, 5.0, 0.75, 2.25, 2.207853215436814]
]

threads_data = [
    ['deepseek-r1:14b', 2150, 'ast', 53.0, 6.5, 0.0, 0.0, 1.3],
    ['deepseek-r1:32b', 1600, 'ast', 48.0, 11.5, 0.7, 0.0, 1.2],
    ['qwen2.5:32b', 240, 'ast', 50.5, 5.5, 0.4, 0.0, 1.7],
    ['mistral-small:latest', 600, 'ast', 56.5, 5.5, 0.4, 0.0, 1.5],
    ['llama3.1:latest', 60, 'ast', 51.0, 5.5, 0.4, 0.0, 2.1],
    ['deepseek-r1:14b', 3500, 'LLM', 72.5, 8.0, 2.0, 1.3, 1.05],
    ['deepseek-r1:32b', 4500, 'LLM', 70.5, 7.5, 1.8, 1.8, 2.6],
    ['qwen2.5:32b', 1200, 'LLM', 65.0, 6.5, 1.3, 3.0, 1.95],
    ['mistral-small:latest', 1050, 'LLM', 64.0, 7.0, 1.8, 3.5, 1.2],
    ['llama3.1:latest', 120, 'LLM', 62.0, 6.5, 1.3, 4.0, 2.7]
]

generate_graphs(arrays_data, 'Arrays')
generate_graphs(djikstra_data, 'Djikstra')
generate_graphs(linked_lists_data, 'Linked_Lists')
generate_graphs(threads_data, 'Threads')