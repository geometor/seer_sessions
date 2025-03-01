import numpy as np

def transform(input_grid):
    # Initialize output_grid
    input_rows, input_cols = input_grid.shape
    output_rows, output_cols = input_rows * 2 + 1, input_cols * 3
    output_grid = np.zeros((output_rows, output_cols), dtype=int)

    # Change output pixels according to the described pattern
    for i in range(input_rows):
        # First row of the pattern
        for j in range(input_cols):
            output_grid[i * 2, j * 3] = input_grid[i, j]
            output_grid[i * 2, j * 3 + 1] = 0
            output_grid[i * 2, j * 3 + 2] = 8

        # Second row of the pattern
        output_grid[i * 2 + 1, :] = 0

        # Third row of the pattern
        if i*2+2 < output_rows: # making sure not to exceed boundaries
            output_grid[i*2 + 2, 0] = 8
            output_grid[i*2 + 2, 1] = 0
            output_grid[i*2 + 2, 2] = 8
            output_grid[i*2 + 2, 3] = 8
            output_grid[i*2 + 2, 4] = 0
            output_grid[i*2 + 2, 5] = 8
            output_grid[i*2 + 2, 6] = 8
            output_grid[i*2 + 2, 7] = 0
            output_grid[i*2 + 2, 8] = 8
    return output_grid

# Example Inputs (from the provided image, represented as numpy arrays)
input_0 = np.array([[2, 2, 2], [2, 4, 2], [2, 2, 2]])
input_1 = np.array([[6, 6, 6], [6, 6, 6]])
input_2 = np.array([[7]])
input_3 = np.array([[1, 2], [3, 5]])

# Expected Outputs (from the provided image, represented as numpy arrays)
expected_output_0 = np.array([[2, 0, 8, 2, 0, 8, 2, 0, 8], [0, 0, 0, 0, 0, 0, 0, 0, 0], [8, 0, 8, 8, 0, 8, 8, 0, 8], [2, 0, 8, 4, 0, 8, 2, 0, 8], [0, 0, 0, 0, 0, 0, 0, 0, 0], [8, 0, 8, 8, 0, 8, 8, 0, 8], [2, 0, 8, 2, 0, 8, 2, 0, 8], [0, 0, 0, 0, 0, 0, 0, 0, 0], [8, 0, 8, 8, 0, 8, 8, 0, 8]])
expected_output_1 = np.array([[6, 0, 8, 6, 0, 8, 6, 0, 8], [0, 0, 0, 0, 0, 0, 0, 0, 0], [8, 0, 8, 8, 0, 8, 8, 0, 8], [6, 0, 8, 6, 0, 8, 6, 0, 8], [0, 0, 0, 0, 0, 0, 0, 0, 0], [8, 0, 8, 8, 0, 8, 8, 0, 8]])
expected_output_2 = np.array([[7, 0, 8], [0, 0, 0], [8, 0, 8]])
expected_output_3 = np.array([[1, 0, 8, 2, 0, 8], [0, 0, 0, 0, 0, 0], [8, 0, 8, 8, 0, 8], [3, 0, 8, 5, 0, 8], [0, 0, 0, 0, 0, 0], [8, 0, 8, 8, 0, 8]])


inputs = [input_0, input_1, input_2, input_3]
expected_outputs = [expected_output_0, expected_output_1, expected_output_2, expected_output_3]

for i, (input_grid, expected_output) in enumerate(zip(inputs, expected_outputs)):
    actual_output = transform(input_grid)
    print(f"Example {i}:")
    print(f"Input:\n{input_grid}")
    print(f"Expected Output:\n{expected_output}")
    print(f"Actual Output:\n{actual_output}")
    match = np.array_equal(actual_output, expected_output)
    print(f"Outputs Match: {match}")
    if not match:
      print(f"Difference: \n {expected_output - actual_output}")
    print("-" * 20)
