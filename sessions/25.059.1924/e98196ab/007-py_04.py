import numpy as np

def analyze_grids(task):
    results = []
    for example in task['train']:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])

        input_azure_count = np.sum(input_grid == 8)
        output_azure_count = np.sum(output_grid == 8)
        input_has_blue = np.any(input_grid==1)
        output_has_blue = np.any(output_grid==1)

        results.append({
            'input_azure_count': int(input_azure_count),
            'output_azure_count': int(output_azure_count),
            'input_has_blue': bool(input_has_blue),
            'output_has_blue': bool(output_has_blue)
        })
    return results

# the task data would be loaded from the json here
# but i will define it as a literal to make the example reproducible

task = {
    "train": [
        {
            "input": [[8, 1, 1], [8, 1, 1], [5, 1, 8]],
            "output": [[8, 0, 0], [8, 0, 0], [0, 0, 8]],
        },
        {
            "input": [[8, 2, 8, 2, 8], [2, 8, 2, 8, 2], [8, 2, 8, 2, 8]],
            "output": [[8, 0, 8, 0, 8], [0, 8, 0, 8, 0], [8, 0, 8, 0, 8]],
        },
        {
            "input": [[8, 8, 8, 8], [8, 2, 8, 2], [8, 5, 8, 8]],
            "output": [[8, 8, 8, 8], [8, 0, 8, 0], [8, 0, 8, 8]],
        },
        {
            "input": [[8, 8, 8, 8, 8], [8, 8, 3, 8, 8], [8, 8, 8, 8, 8]],
            "output": [[8, 8, 8, 8, 8], [8, 8, 0, 8, 8], [8, 8, 8, 8, 8]],
        },
    ]
}
analysis_results = analyze_grids(task)
print(analysis_results)

