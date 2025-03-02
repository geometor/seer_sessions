def analyze_grid(grid):
    """
    Analyzes a single grid and returns relevant metrics.
    """
    magenta_count = np.sum(grid == 6)
    white_count = np.sum(grid == 0)
    other_count = grid.size - magenta_count - white_count
    shape = grid.shape
    return {
        'magenta_count': magenta_count,
        'white_count': white_count,
        'other_count': other_count,
        'shape': shape
    }

def compare_grids(input_grid, expected_output_grid, actual_output_grid):
    """
    Compares the expected and actual output grids.
    """
    match = np.array_equal(expected_output_grid, actual_output_grid)
    return {
        'match': match
    }


task_data = [
    {
        'input': np.array([[6, 0, 0], [0, 6, 6], [0, 0, 0]]),
        'output': np.array([[6, 0, 0], [6, 0, 0], [0, 0, 0]])
    },
    {
        'input': np.array([[6, 0, 0], [0, 0, 6], [0, 0, 0]]),
        'output': np.array([[6, 0, 0], [6, 0, 0], [0, 0, 0]])
    },
    {
        'input': np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]]),
        'output': np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
    },
     {
        'input': np.array([[6, 0, 0, 0], [0, 0, 0, 6], [0, 0, 0, 0], [0, 6, 0, 0]]),
        'output': np.array([[6, 0, 0], [6, 0, 0], [6, 0, 0], [0, 0, 0]])
    },
    {
        'input': np.array([[0, 6, 0, 0], [0, 0, 0, 0], [0, 0, 6, 0], [0, 0, 0, 0]]),
        'output': np.array([[6, 0, 0], [6, 0, 0], [0, 0, 0], [0, 0, 0]])
    }

]

results = []
for i, example in enumerate(task_data):
    input_analysis = analyze_grid(example['input'])
    output_analysis = analyze_grid(example['output'])
    actual_output = transform(example['input'])
    comparison = compare_grids(example['output'], actual_output)
    results.append({
        'example_index': i,
        'input': input_analysis,
        'output': output_analysis,
        'comparison': comparison
    })

import yaml
print(yaml.dump(results))
