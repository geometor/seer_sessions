import numpy as np

def get_grid_dimensions(grid):
    return grid.shape

def array_to_string(arr):
    return np.array2string(arr, separator=', ')


def analyze_results(task):
    results = []
    for example in task['train']:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        predicted_output = transform(input_grid)  # Assuming 'transform' function from the provided code
        dimensions = get_grid_dimensions(input_grid)
        match = np.array_equal(output_grid, predicted_output)
        results.append({
            'input_dimensions': dimensions,
            'match': match,
            'input': array_to_string(input_grid),
            'expected_output': array_to_string(output_grid),
            'predicted_output': array_to_string(predicted_output),
            
        })
    return results

task = {
    'train': [
        {'input': [[0, 0, 5, 0, 0], [0, 0, 5, 0, 0], [0, 0, 5, 0, 0]], 'output': [[0, 0, 5, 0, 0], [0, 0, 5, 0, 0], [0, 0, 5, 0, 0]]},
        {'input': [[0, 0, 8, 0, 0, 0], [0, 0, 8, 0, 0, 0], [0, 0, 8, 0, 0, 0], [0, 0, 8, 0, 0, 0]], 'output': [[0, 0, 0, 0, 0, 0], [0, 0, 8, 0, 0, 0], [0, 0, 8, 0, 0, 0], [0, 0, 0, 0, 0, 0]]},
        {'input': [[0, 3, 0, 0, 0], [0, 3, 0, 0, 0], [0, 3, 0, 0, 0], [0, 3, 0, 0, 0], [0, 3, 0, 0, 0]], 'output': [[0, 3, 0, 0, 0], [0, 3, 0, 0, 0], [0, 3, 0, 0, 0], [0, 3, 0, 0, 0], [0, 3, 0, 0, 0]]}
    ]
}

results = analyze_results(task)

for i, result in enumerate(results):
    print(f"Example {i+1}:")
    print(f"  Input Dimensions: {result['input_dimensions']}")
    print(f"  Match: {result['match']}")
    print(f"  Input: {result['input']}")
    print(f"  Expected Output: {result['expected_output']}")
    print(f"  Predicted Output: {result['predicted_output']}")
    print("-" * 20)
