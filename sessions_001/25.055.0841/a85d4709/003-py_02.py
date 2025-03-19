import numpy as np

def analyze_results(examples, transform_func):
    results = []
    for i, (input_grid, expected_output) in enumerate(examples):
        input_grid = np.array(input_grid)
        expected_output = np.array(expected_output)
        actual_output = transform_func(input_grid)
        match = np.array_equal(actual_output, expected_output)
        results.append({
            "example_index": i,
            "input_shape": input_grid.shape,
            "output_shape": expected_output.shape,
            "match": match,
            "differences": np.where(actual_output != expected_output) if not match else None
        })
    return results

# Example Usage (replace with actual task data later):
examples = [
    ([[0, 0, 0], [0, 5, 0], [0, 0, 0]], [[3, 3, 3], [3, 4, 3], [3, 3, 3]]),
    ([[5, 0, 5], [0, 0, 0], [5, 0, 5]], [[4, 3, 4], [3, 3, 3], [4, 3, 4]]),
    ([[5, 5, 5], [5, 0, 5], [5, 5, 5]], [[4, 4, 4], [4, 3, 4], [4, 4, 4]]),
]

previous_code = """
import numpy as np

def transform(input_grid):
    # initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # change output pixels based on the substitution rules
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            if output_grid[i, j] == 0:
                output_grid[i, j] = 3
            elif output_grid[i, j] == 5:
                output_grid[i, j] = 4
            else:
                output_grid[i, j] = 2

    return output_grid
"""

# Extract the transform function from the code
exec(previous_code)  # Define the transform function

results = analyze_results(examples, transform)

for result in results:
    print(f"Example {result['example_index'] + 1}:")
    print(f"  Input Shape: {result['input_shape']}")
    print(f"  Output Shape: {result['output_shape']}")
    print(f"  Match: {result['match']}")
    if not result['match']:
        print(f"  Differences (row, col): {result['differences']}")