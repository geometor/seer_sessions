import numpy as np

def analyze_results(input_grid, expected_output, actual_output):
    input_grid = np.array(input_grid)
    expected_output = np.array(expected_output)
    actual_output = np.array(actual_output)

    input_shape = input_grid.shape
    expected_shape = expected_output.shape
    actual_shape = actual_output.shape

    match = np.array_equal(expected_output, actual_output)

    print(f"  Input Shape: {input_shape}")
    print(f"  Expected Output Shape: {expected_shape}")
    print(f"  Actual Output Shape: {actual_shape}")
    print(f"  Match: {match}")
    if not match:
        diff = expected_output - actual_output
        print(f"  Difference:\n{diff}")
    else:
      print("  No difference")

#Example Usage
example_input_grids = [
    [[3, 3, 3, 4, 2, 2, 8, 8, 8, 9], [3, 3, 3, 4, 2, 2, 8, 8, 8, 9], [3, 3, 3, 4, 2, 2, 8, 8, 8, 9]],
    [[0, 0, 0, 7, 0, 0, 0, 7, 0, 0], [0, 0, 0, 7, 0, 0, 0, 7, 0, 0], [0, 0, 0, 7, 0, 0, 0, 7, 0, 0], [0, 0, 0, 7, 0, 0, 0, 7, 0, 0], [0, 0, 0, 7, 0, 0, 0, 7, 0, 0], [0, 0, 0, 7, 0, 0, 0, 7, 0, 0], [0, 0, 0, 7, 0, 0, 0, 7, 0, 0]],
    [[6, 6, 5, 5, 5, 5, 5, 5, 5, 6], [6, 6, 5, 5, 5, 5, 5, 5, 5, 6], [6, 5, 5, 5, 5, 5, 5, 5, 5, 5], [6, 6, 6, 5, 5, 5, 5, 5, 6, 6], [6, 6, 6, 5, 5, 5, 5, 5, 6, 6]],

]

example_output_grids = [
    [[4, 2, 9, 4], [4, 2, 9, 4], [4, 2, 9, 4]],
    [[7, 7, 0, 0], [7, 7, 0, 0], [7, 7, 0, 0], [7, 7, 0, 0], [7, 7, 0, 0], [7, 7, 0, 0]],
    [[5, 5, 5, 5], [5, 5, 5, 5], [5, 5, 5, 5], [5, 5, 5, 5], [5, 5, 5, 5]]
]

example_actual_outputs = [
    transform(example_input_grids[0]), transform(example_input_grids[1]), transform(example_input_grids[2])
]

for i in range(len(example_input_grids)):
    print(f"Example {i+1}:")
    analyze_results(example_input_grids[i], example_output_grids[i], example_actual_outputs[i])
