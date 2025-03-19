# Simulated Code Execution (using a basic identity transform)
import numpy as np

def transform(input_grid):
    """
    A basic identity transform for initial testing.
    Copies input grid to output, preserving shape.
    """
    return np.copy(input_grid)

def analyze_results(task):
    results = []
    for example in task['train']:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        predicted_output = transform(input_grid)

        input_rows, input_cols = input_grid.shape
        output_rows, output_cols = output_grid.shape

        input_color_counts = {color: np.sum(input_grid == color) for color in range(10)}
        output_color_counts = {color: np.sum(output_grid == color) for color in range(10)}
        predicted_output_counts = {color: np.sum(predicted_output==color) for color in range(10)}

        match = np.array_equal(predicted_output, output_grid)

        results.append({
            'input_shape': (input_rows, input_cols),
            'output_shape': (output_rows, output_cols),
            'input_color_counts': input_color_counts,
            'output_color_counts': output_color_counts,
            'predicted_output_counts' : predicted_output_counts,
            'match': match
        })
    return results

# Using the same 'task' as provided
analysis = analyze_results(task)
for i, result in enumerate(analysis):
    print(f"Example {i+1}:")
    print(f"  Input Shape: {result['input_shape']}")
    print(f"  Output Shape: {result['output_shape']}")
    print(f"  Input Color Counts: {result['input_color_counts']}")
    print(f"  Output Color Counts: {result['output_color_counts']}")
    print(f"  Predicted Output Counts: {result['predicted_output_counts']}")
    print(f"  Match: {result['match']}")
    print("-" * 20)