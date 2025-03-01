import numpy as np

def code_execution(input_grid, output_grid, predicted_grid):
    """Executes code to analyze the transformation."""

    # 1. Check if output_grid and predicted_grid are identical
    grids_match = np.array_equal(output_grid, predicted_grid)

    # 2. Analyze differences if they don't match
    diff_positions = []
    if not grids_match:
        diff_positions = np.where(output_grid != predicted_grid)
        diff_positions = list(zip(diff_positions[0], diff_positions[1]))

    print(f"Grids Match: {grids_match}")
    print(f"Difference Positions: {diff_positions}")


# Example usage (replace with actual data from each example)
input_grid_ex1 = np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
output_grid_ex1 = np.array([[8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

predicted_grid_ex1 = transform(input_grid_ex1)
code_execution(input_grid_ex1, output_grid_ex1, predicted_grid_ex1)

input_grid_ex2 = np.array([[1, 1, 1, 1, 1, 1, 1, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8]])
output_grid_ex2 = np.array([[1, 1, 1, 1, 1, 1, 1, 8, 8, 8],[1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])

predicted_grid_ex2 = transform(input_grid_ex2)
code_execution(input_grid_ex2, output_grid_ex2, predicted_grid_ex2)

input_grid_ex3 = np.array([[8, 8, 8, 1, 1, 1, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8]])
output_grid_ex3 = np.array([[8, 8, 8, 1, 1, 1, 8, 8, 8, 8], [8, 8, 8, 1, 1, 1, 1, 1, 8, 8]])

predicted_grid_ex3 = transform(input_grid_ex3)
code_execution(input_grid_ex3, output_grid_ex3, predicted_grid_ex3)

input_grid_ex4 = np.array([
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [8, 8, 8, 8, 8, 8, 8, 8, 0, 0],
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
    [8, 5, 8, 8, 8, 8, 8, 8, 8, 8]
])

output_grid_ex4 = np.array([
    [8, 8, 8, 8, 8, 8, 8, 8, 8, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 0, 0],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [8, 5, 2, 2, 2, 2, 2, 2, 2, 2]
])
predicted_grid_ex4 = transform(input_grid_ex4)
code_execution(input_grid_ex4, output_grid_ex4, predicted_grid_ex4)