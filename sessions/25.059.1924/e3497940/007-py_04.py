import numpy as np

def describe_grid(grid):
    """Provides a concise description of a grid."""
    return f"Shape: {grid.shape}, Colors: {np.unique(grid)}"

def analyze_results(task_examples, transform_function):
    """Analyzes results of applying transform to input grids."""
    results = []
    for example in task_examples:
        input_grid = np.array(example['input'])
        expected_output_grid = np.array(example['output'])
        transformed_grid = transform_function(input_grid)
        is_correct = np.array_equal(transformed_grid, expected_output_grid)
        results.append({
            'input_description': describe_grid(input_grid),
            'expected_output_description': describe_grid(expected_output_grid),
            'transformed_grid_description': describe_grid(transformed_grid),
            'is_correct': is_correct
        })
    return results

# Assuming 'task' variable holds the ARC task data
# Example Usage (replace with actual task data)
task = [
    {'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 5, 0, 0, 0, 0], [0, 0, 0, 0, 5, 0, 0, 0, 0], [0, 0, 0, 0, 5, 0, 0, 0, 0], [0, 0, 0, 0, 5, 0, 0, 0, 0], [0, 0, 0, 0, 5, 0, 0, 0, 0], [0, 0, 0, 0, 5, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]], 'output': [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]},
    {'input': [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 5, 5, 5, 5, 5, 0], [0, 0, 5, 5, 5, 5, 5, 0], [0, 0, 5, 5, 5, 5, 5, 0], [0, 0, 5, 5, 5, 5, 5, 0], [0, 0, 5, 5, 5, 5, 5, 0], [0, 0, 0, 0, 0, 0, 0, 0]], 'output': [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]},
    {'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 5, 0, 0, 0, 0], [0, 0, 0, 4, 5, 4, 0, 0, 0], [0, 0, 4, 4, 5, 4, 4, 0, 0], [0, 4, 4, 4, 5, 4, 4, 4, 0], [0, 0, 0, 0, 5, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]], 'output': [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 4, 4, 0, 0, 0], [0, 0, 4, 4, 4, 4, 0, 0], [0, 4, 4, 4, 4, 4, 4, 4, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]},
    {'input': [[0, 0, 0, 0, 0, 0, 0, 0], [0, 5, 5, 5, 5, 5, 5, 0], [0, 5, 5, 5, 5, 5, 5, 0], [0, 5, 5, 5, 5, 5, 5, 0], [0, 5, 5, 5, 5, 5, 5, 0], [0, 0, 0, 0, 0, 0, 0, 0]], 'output': [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]},
    {'input': [[0, 0, 0, 5, 0, 0, 0, 0], [0, 0, 5, 4, 5, 0, 0, 0], [0, 0, 5, 4, 5, 0, 0, 0], [0, 5, 4, 4, 4, 5, 0, 0], [0, 0, 5, 4, 5, 0, 0, 0], [0, 0, 0, 5, 0, 0, 0, 0]], 'output': [[0, 0, 0, 0, 0, 0, 0], [0, 0, 4, 0, 0, 0, 0], [0, 0, 4, 0, 0, 0, 0], [0, 4, 4, 4, 0, 0, 0], [0, 0, 4, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]}
]

results = analyze_results(task, transform)
for i, res in enumerate(results):
    print(f"Example {i+1}:")
    print(f"  Input:       {res['input_description']}")
    print(f"  Expected Out: {res['expected_output_description']}")
    print(f"  Transformed:  {res['transformed_grid_description']}")
    print(f"  Correct:     {res['is_correct']}")