import numpy as np

def analyze_examples(task_data):
    """Analyzes input/output pairs for differences and gathers color counts."""
    results = []
    for example in task_data['train']:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])

        # Check for differences
        differences = np.sum(input_grid != output_grid)
        diff_positions = []
        if differences > 0:
          diff_positions = np.argwhere(input_grid != output_grid).tolist()
        
        # Count colors in input grid
        unique_colors, counts = np.unique(input_grid, return_counts=True)
        color_counts = dict(zip(unique_colors, counts))

        results.append({
            'example_id': example.get('id', 'N/A'),  # Assuming 'id' might be present
            'differences': differences,
            'diff_positions': diff_positions,
            'input_color_counts': color_counts
        })
    return results

# Example Usage (replace with actual task data)
# ARC data structure
#   task_data["train"] = list of training examples, each a dict with "input" and "output"
#   task_data["test"] = list of test examples, each a dict with "input" and "output" (usually only one test example)
task_data = {
    "train": [
        {"input": [[1, 1], [1, 1]], "output": [[1, 1], [1, 1]]},
        {"input": [[2, 3], [4, 5]], "output": [[2, 3], [4, 5]]},
        {"input": [[0, 6, 9], [7, 8, 0], [5,5,5]], "output": [[0, 6, 9], [7, 8, 0], [5,5,5]]},
    ],
    "test": [
        {"input": [[1]], "output": [[1]]}
    ]
}
analysis_results = analyze_examples(task_data)
print(analysis_results)
