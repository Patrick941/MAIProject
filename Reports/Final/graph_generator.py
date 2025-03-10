import csv
import numpy as np
from statistics import mean
from collections import defaultdict
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

    bar1 = ax1.bar(index, times, bar_width, label='Time (s)', color='skyblue')
    ax1.set_xlabel('Model and Bug Type')
    ax1.set_ylabel('Time (s)')
    ax1.tick_params(axis='y')

    ax2 = ax1.twinx()
    bar2 = ax2.bar(index + bar_width, attempts, bar_width, label='Attempts', color='lightgreen')
    ax2.set_ylabel('Attempts')
    ax2.tick_params(axis='y')

    ax1.set_xticks(index + bar_width / 2)
    ax1.set_xticklabels(labels, rotation=45, ha='right')

    fig.tight_layout()
    plt.title('Model and Bug Insertion Comparison', pad=20)
    fig.legend(loc='upper right', bbox_to_anchor=(1,1), bbox_transform=ax1.transAxes)
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

    bar1 = ax1.bar(index, cognitive_complexity, bar_width, label='Cognitive Complexity', color='lightblue')
    ax1.set_xlabel('Model and Bug Type')
    ax1.set_ylabel('Cognitive Complexity')
    ax1.tick_params(axis='y')

    ax2 = ax1.twinx()
    bar2 = ax2.bar(index + bar_width, cyclomatic_complexity, bar_width, label='Cyclomatic Complexity', color='lightcoral')
    ax2.set_ylabel('Cyclomatic Complexity')
    ax2.tick_params(axis='y')

    ax3 = ax1.twinx()
    ax3.spines['right'].set_position(('outward', 60))
    bar3 = ax3.bar(index + 2 * bar_width, inverse_similarity_scores, bar_width, label='Diversity Score', color='lightgreen')
    ax3.set_ylabel('Diversity Score')
    ax3.tick_params(axis='y')

    ax1.set_xticks(index + bar_width)
    ax1.set_xticklabels(labels, rotation=45, ha='right')

    fig.tight_layout()
    plt.title('Model and Bug Insertion Complexity and Diversity Comparison', pad=20)
    fig.legend(loc='upper right', bbox_to_anchor=(1,1), bbox_transform=ax1.transAxes)
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
   

def generate_hyperparameter_graphs(hyperparam_data, param_name):
    import matplotlib.pyplot as plt

    # Add derived fields
    for row in hyperparam_data:
        row['combined_attempts'] = row['code_generation_attempts'] + row['bug_insertion_attempts']
        row['diversity_score'] = 1 / row['similarity_score'] if row['similarity_score'] else float('inf')

    # Group data by hyperparameter value
    grouped = defaultdict(list)
    for row in hyperparam_data:
        grouped[row[param_name]].append(row)

    # Prepare data for runtime vs attempts
    labels, runtimes, attempts = [], [], []
    for val in sorted(grouped.keys()):
        entries = grouped[val]
        labels.append(str(val))
        runtimes.append(mean(e['runtime'] for e in entries))
        attempts.append(mean(e['combined_attempts'] for e in entries))

    # Prepare data for complexities and diversity
    cog_comp, cyc_comp, div_score = [], [], []
    for val in sorted(grouped.keys()):
        entries = grouped[val]
        cog_comp.append(mean(e['cognitive_complexity'] for e in entries))
        cyc_comp.append(mean(e['cyclomatic_complexity'] for e in entries))
        div_score.append(mean(e['diversity_score'] for e in entries))

    # Create a single figure with two subplots
    fig, (ax_top, ax_bottom) = plt.subplots(2, 1, figsize=(14, 12))

    # First subplot: runtime vs attempts
    bar_width = 0.3
    index = np.arange(len(labels))
    bar1 = ax_top.bar(index, runtimes, bar_width, label='Runtime', color='skyblue')
    ax_top.set_xlabel(param_name)
    ax_top.set_ylabel('Runtime (s)')
    ax_top.tick_params(axis='y')
    ax_top.set_xticks(index + bar_width / 2)
    ax_top.set_xticklabels(labels, rotation=45, ha='right')

    ax_top_twin = ax_top.twinx()
    bar2 = ax_top_twin.bar(index + bar_width, attempts, bar_width, label='Attempts', color='lightgreen')
    ax_top_twin.set_ylabel('Attempts')
    ax_top_twin.tick_params(axis='y')

    # Second subplot: cognitive, cyclomatic, diversity (3 y-axes)
    bar_width = 0.2
    index = np.arange(len(labels))
    bar1 = ax_bottom.bar(index, cog_comp, bar_width, label='Cognitive Complexity', color='lightblue')
    ax_bottom.set_xlabel(param_name)
    ax_bottom.set_ylabel('Cognitive Complexity')
    ax_bottom.tick_params(axis='y')
    ax_bottom.set_xticks(index + bar_width)
    ax_bottom.set_xticklabels(labels, rotation=45, ha='right')

    ax_bottom2 = ax_bottom.twinx()
    bar2 = ax_bottom2.bar(index + bar_width, cyc_comp, bar_width, label='Cyclomatic Complexity', color='lightcoral')
    ax_bottom2.set_ylabel('Cyclomatic Complexity')
    ax_bottom2.tick_params(axis='y')

    ax_bottom3 = ax_bottom.twinx()
    ax_bottom3.spines['right'].set_position(('outward', 60))
    bar3 = ax_bottom3.bar(index + 2 * bar_width, div_score, bar_width, label='Diversity Score', color='lightgreen')
    ax_bottom3.set_ylabel('Diversity Score')
    ax_bottom3.tick_params(axis='y')

    fig.tight_layout()
    fig.legend(loc='upper right', bbox_to_anchor=(1,1), bbox_transform=ax_bottom.transAxes)
    plt.savefig(f'Images/Hyperparam_{param_name}_Comparison.png')
    plt.close()
        
temperature_data = [
    {'temperature': 0.001, 'runtime': 194, 'cognitive_complexity': 56.54932628534889, 'cyclomatic_complexity': 4.25, 'code_generation_attempts': 0.5, 'bug_insertion_attempts': 0.0, 'similarity_score': 1.9655366098262044},
    {'temperature': 0.002, 'runtime': 307, 'cognitive_complexity': 56.54932628534889, 'cyclomatic_complexity': 4.25, 'code_generation_attempts': 0.5, 'bug_insertion_attempts': 0.0, 'similarity_score': 1.9655366098262044},
    {'temperature': 0.004, 'runtime': 260, 'cognitive_complexity': 55.70768474447835, 'cyclomatic_complexity': 5.0, 'code_generation_attempts': 1.25, 'bug_insertion_attempts': 0.0, 'similarity_score': 2.4652825970800487},
    {'temperature': 0.008, 'runtime': 151, 'cognitive_complexity': 56.87723560340458, 'cyclomatic_complexity': 3.25, 'code_generation_attempts': 0.25, 'bug_insertion_attempts': 0.0, 'similarity_score': 1.7248935626527073},
    {'temperature': 0.016, 'runtime': 158, 'cognitive_complexity': 65.25870537984157, 'cyclomatic_complexity': 2.75, 'code_generation_attempts': 0.25, 'bug_insertion_attempts': 0.0, 'similarity_score': 1.4698105141180549},
    {'temperature': 0.032, 'runtime': 230, 'cognitive_complexity': 58.85449466848282, 'cyclomatic_complexity': 3.0, 'code_generation_attempts': 0.75, 'bug_insertion_attempts': 0.0, 'similarity_score': 1.5569735674717782},
    {'temperature': 0.064, 'runtime': 331, 'cognitive_complexity': 66.1475483007262, 'cyclomatic_complexity': 2.75, 'code_generation_attempts': 1.75, 'bug_insertion_attempts': 0.0, 'similarity_score': 1.4483874678958113},
    {'temperature': 0.128, 'runtime': 164, 'cognitive_complexity': 56.34794856180849, 'cyclomatic_complexity': 3.25, 'code_generation_attempts': 0.25, 'bug_insertion_attempts': 0.0, 'similarity_score': 1.332241565584618},
    {'temperature': 0.256, 'runtime': 116, 'cognitive_complexity': 55.42147105947762, 'cyclomatic_complexity': 5.0, 'code_generation_attempts': 0.0, 'bug_insertion_attempts': 0.0, 'similarity_score': 2.1457167569377433},
    {'temperature': 0.512, 'runtime': 193, 'cognitive_complexity': 58.41115138255944, 'cyclomatic_complexity': 4.25, 'code_generation_attempts': 0.75, 'bug_insertion_attempts': 0.0, 'similarity_score': 1.2660534386737279},
    {'temperature': 1.024, 'runtime': 129, 'cognitive_complexity': 55.788091836026, 'cyclomatic_complexity': 4.25, 'code_generation_attempts': 0.0, 'bug_insertion_attempts': 0.0, 'similarity_score': 1.906223444704691},
    {'temperature': 2.048, 'runtime': 184, 'cognitive_complexity': 61.884398244165844, 'cyclomatic_complexity': 4.5, 'code_generation_attempts': 0.5, 'bug_insertion_attempts': 0.0, 'similarity_score': 1.6355270900238865},
    {'temperature': 4.096, 'runtime': 133, 'cognitive_complexity': 61.884398244165844, 'cyclomatic_complexity': 4.5, 'code_generation_attempts': 0.5, 'bug_insertion_attempts': 0.0, 'similarity_score': 1.6355270900238865},
    {'temperature': 8.192, 'runtime': 284, 'cognitive_complexity': 56.959005255632704, 'cyclomatic_complexity': 4.25, 'code_generation_attempts': 1.25, 'bug_insertion_attempts': 0.0, 'similarity_score': 1.9839866872651846},
    {'temperature': 16.384, 'runtime': 233, 'cognitive_complexity': 56.959005255632704, 'cyclomatic_complexity': 4.25, 'code_generation_attempts': 1.25, 'bug_insertion_attempts': 0.0, 'similarity_score': 1.9839866872651846},
    {'temperature': 32.768, 'runtime': 129, 'cognitive_complexity': 56.959005255632704, 'cyclomatic_complexity': 4.25, 'code_generation_attempts': 1.25, 'bug_insertion_attempts': 0.0, 'similarity_score': 1.9839866872651846},
    {'temperature': 65.536, 'runtime': 233, 'cognitive_complexity': 58.544563417254615, 'cyclomatic_complexity': 3.75, 'code_generation_attempts': 1.0, 'bug_insertion_attempts': 0.0, 'similarity_score': 1.6079502324501929}
]

max_tokens_data = [
    {'max_tokens': 10, 'runtime': 325, 'cognitive_complexity': 55.28328923131547, 'cyclomatic_complexity': 5.0, 'code_generation_attempts': 1.75, 'bug_insertion_attempts': 0.0, 'similarity_score': 2.0935738210261317},
    {'max_tokens': 16, 'runtime': 301, 'cognitive_complexity': 54.69337315286633, 'cyclomatic_complexity': 5.0, 'code_generation_attempts': 1.5, 'bug_insertion_attempts': 0.0, 'similarity_score': 1.9840382636472813},
    {'max_tokens': 26, 'runtime': 190, 'cognitive_complexity': 55.65977558309831, 'cyclomatic_complexity': 4.25, 'code_generation_attempts': 0.5, 'bug_insertion_attempts': 0.0, 'similarity_score': 1.7562192023459997},
    {'max_tokens': 41, 'runtime': 183, 'cognitive_complexity': 55.967453877175004, 'cyclomatic_complexity': 4.75, 'code_generation_attempts': 0.5, 'bug_insertion_attempts': 0.0, 'similarity_score': 2.32090576730472},
    {'max_tokens': 66, 'runtime': 205, 'cognitive_complexity': 55.967453877175004, 'cyclomatic_complexity': 4.75, 'code_generation_attempts': 0.5, 'bug_insertion_attempts': 0.0, 'similarity_score': 2.32090576730472},
    {'max_tokens': 105, 'runtime': 271, 'cognitive_complexity': 55.967453877175004, 'cyclomatic_complexity': 4.75, 'code_generation_attempts': 0.5, 'bug_insertion_attempts': 0.0, 'similarity_score': 2.32090576730472},
    {'max_tokens': 168, 'runtime': 161, 'cognitive_complexity': 55.432413858433684, 'cyclomatic_complexity': 4.0, 'code_generation_attempts': 0.25, 'bug_insertion_attempts': 0.0, 'similarity_score': 1.3129142055371195},
    {'max_tokens': 268, 'runtime': 148, 'cognitive_complexity': 55.61829975715055, 'cyclomatic_complexity': 5.0, 'code_generation_attempts': 0.25, 'bug_insertion_attempts': 0.0, 'similarity_score': 2.5678363503457144},
    {'max_tokens': 429, 'runtime': 246, 'cognitive_complexity': 55.66814970960912, 'cyclomatic_complexity': 5.0, 'code_generation_attempts': 1.0, 'bug_insertion_attempts': 0.0, 'similarity_score': 2.075705709488241},
    {'max_tokens': 687, 'runtime': 237, 'cognitive_complexity': 56.98767029000747, 'cyclomatic_complexity': 3.25, 'code_generation_attempts': 1.0, 'bug_insertion_attempts': 0.0, 'similarity_score': 1.3750930813315745},
    {'max_tokens': 1100, 'runtime': 263, 'cognitive_complexity': 56.98767029000747, 'cyclomatic_complexity': 3.25, 'code_generation_attempts': 1.0, 'bug_insertion_attempts': 0.0, 'similarity_score': 1.3750930813315745},
    {'max_tokens': 1759, 'runtime': 217, 'cognitive_complexity': 62.693951104790926, 'cyclomatic_complexity': 3.5, 'code_generation_attempts': 0.75, 'bug_insertion_attempts': 0.0, 'similarity_score': 1.437570938329928},
    {'max_tokens': 2815, 'runtime': 211, 'cognitive_complexity': 55.27052278838247, 'cyclomatic_complexity': 4.5, 'code_generation_attempts': 0.75, 'bug_insertion_attempts': 0.0, 'similarity_score': 1.77230705799445},
    {'max_tokens': 4504, 'runtime': 233, 'cognitive_complexity': 57.1439778075115, 'cyclomatic_complexity': 4.0, 'code_generation_attempts': 1.0, 'bug_insertion_attempts': 0.0, 'similarity_score': 1.8764360888057423}
]

top_k_data = [
    {'top_k': 1.0, 'runtime': 193, 'cognitive_complexity': 55.070839960357304, 'cyclomatic_complexity': 4.0, 'code_generation_attempts': 0.5, 'bug_insertion_attempts': 0.0, 'similarity_score': 1.3237073998418383},
    {'top_k': 1.6, 'runtime': 122, 'cognitive_complexity': 56.635919111462684, 'cyclomatic_complexity': 4.5, 'code_generation_attempts': 0.0, 'bug_insertion_attempts': 0.0, 'similarity_score': 1.8652211935877359},
    {'top_k': 2.56, 'runtime': 152, 'cognitive_complexity': 55.67874553703072, 'cyclomatic_complexity': 3.5, 'code_generation_attempts': 0.25, 'bug_insertion_attempts': 0.0, 'similarity_score': 1.686279123866499},
    {'top_k': 4.096, 'runtime': 218, 'cognitive_complexity': 55.79706973180615, 'cyclomatic_complexity': 5.0, 'code_generation_attempts': 0.75, 'bug_insertion_attempts': 0.0, 'similarity_score': 2.503582527983327},
    {'top_k': 6.5536, 'runtime': 299, 'cognitive_complexity': 57.836859818741004, 'cyclomatic_complexity': 4.0, 'code_generation_attempts': 0.6666666666666666, 'bug_insertion_attempts': 0.0, 'similarity_score': 1.6300998611106432},
    {'top_k': 10.4858, 'runtime': 151, 'cognitive_complexity': 54.963199305700236, 'cyclomatic_complexity': 3.5, 'code_generation_attempts': 0.0, 'bug_insertion_attempts': 0.0, 'similarity_score': 1.3373514709454153},
    {'top_k': 16.7772, 'runtime': 283, 'cognitive_complexity': 54.54287042206297, 'cyclomatic_complexity': 3.5, 'code_generation_attempts': 1.25, 'bug_insertion_attempts': 0.0, 'similarity_score': 1.4865061838227875},
    {'top_k': 26.8435, 'runtime': 248, 'cognitive_complexity': 55.89924865373773, 'cyclomatic_complexity': 4.5, 'code_generation_attempts': 1.0, 'bug_insertion_attempts': 0.0, 'similarity_score': 1.9394356693121126},
    {'top_k': 42.9497, 'runtime': 236, 'cognitive_complexity': 62.341790791800065, 'cyclomatic_complexity': 3.25, 'code_generation_attempts': 1.0, 'bug_insertion_attempts': 0.0, 'similarity_score': 1.462288144293308},
    {'top_k': 68.7195, 'runtime': 178, 'cognitive_complexity': 56.6919126809029, 'cyclomatic_complexity': 3.5, 'code_generation_attempts': 0.5, 'bug_insertion_attempts': 0.0, 'similarity_score': 1.6967758122207817},
    {'top_k': 109.951, 'runtime': 186, 'cognitive_complexity': 60.83360108645301, 'cyclomatic_complexity': 4.0, 'code_generation_attempts': 0.5, 'bug_insertion_attempts': 0.0, 'similarity_score': 1.6670235179191089},
    {'top_k': 175.922, 'runtime': 203, 'cognitive_complexity': 55.31129609344306, 'cyclomatic_complexity': 3.5, 'code_generation_attempts': 0.5, 'bug_insertion_attempts': 0.0, 'similarity_score': 1.575781886025387}
]

top_p_data = [
    {'top_p': 0.001, 'runtime': 312, 'cognitive_complexity': 58.33483347195039, 'cyclomatic_complexity': 2.75, 'code_generation_attempts': 1.5, 'bug_insertion_attempts': 0.0, 'similarity_score': 1.4414429424568778},
    {'top_p': 0.002, 'runtime': 205, 'cognitive_complexity': 56.07032549735663, 'cyclomatic_complexity': 4.25, 'code_generation_attempts': 0.75, 'bug_insertion_attempts': 0.0, 'similarity_score': 1.7775778685059993},
    {'top_p': 0.004, 'runtime': 309, 'cognitive_complexity': 57.59276266999938, 'cyclomatic_complexity': 3.25, 'code_generation_attempts': 1.5, 'bug_insertion_attempts': 0.0, 'similarity_score': 1.699097380926292},
    {'top_p': 0.008, 'runtime': 228, 'cognitive_complexity': 57.77916724415455, 'cyclomatic_complexity': 3.25, 'code_generation_attempts': 1.0, 'bug_insertion_attempts': 0.0, 'similarity_score': 1.6136477879283522},
    {'top_p': 0.016, 'runtime': 125, 'cognitive_complexity': 56.676443630174646, 'cyclomatic_complexity': 4.25, 'code_generation_attempts': 0.0, 'bug_insertion_attempts': 0.0, 'similarity_score': 1.860808011889075},
    {'top_p': 0.032, 'runtime': 165, 'cognitive_complexity': 56.76777146453086, 'cyclomatic_complexity': 4.25, 'code_generation_attempts': 0.25, 'bug_insertion_attempts': 0.0, 'similarity_score': 1.8204340177672664},
    {'top_p': 0.064, 'runtime': 267, 'cognitive_complexity': 55.54866257762259, 'cyclomatic_complexity': 4.25, 'code_generation_attempts': 1.25, 'bug_insertion_attempts': 0.0, 'similarity_score': 1.7429051830176832},
    {'top_p': 0.128, 'runtime': 185, 'cognitive_complexity': 55.27059176870601, 'cyclomatic_complexity': 4.25, 'code_generation_attempts': 0.5, 'bug_insertion_attempts': 0.0, 'similarity_score': 1.8341035494389755},
    {'top_p': 0.256, 'runtime': 208, 'cognitive_complexity': 58.91581601923888, 'cyclomatic_complexity': 3.25, 'code_generation_attempts': 0.75, 'bug_insertion_attempts': 0.0, 'similarity_score': 1.4879672974215494},
    {'top_p': 0.512, 'runtime': 248, 'cognitive_complexity': 56.47640035729147, 'cyclomatic_complexity': 4.25, 'code_generation_attempts': 1.0, 'bug_insertion_attempts': 0.0, 'similarity_score': 1.7286575147913046},
    {'top_p': 1.024, 'runtime': 131, 'cognitive_complexity': 55.73666053969563, 'cyclomatic_complexity': 3.25, 'code_generation_attempts': 0.0, 'bug_insertion_attempts': 0.0, 'similarity_score': 1.6383440033904262}
]
 
generate_hyperparameter_graphs(temperature_data, 'temperature')
generate_hyperparameter_graphs(max_tokens_data, 'max_tokens')
generate_hyperparameter_graphs(top_k_data, 'top_k')
generate_hyperparameter_graphs(top_p_data, 'top_p')