import numpy as np

def analyze_example(input_grid, output_grid):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    input_height, input_width = input_grid.shape
    output_height, output_width = output_grid.shape
    input_colors = np.unique(input_grid)
    output_colors = np.unique(output_grid)

    print(f"  Input Shape: {input_height}x{input_width}, Colors: {input_colors}")
    print(f"  Output Shape: {output_height}x{output_width}, Colors: {output_colors}")

    # Check for blue in the last row and column of the input
    last_row_colors = np.unique(input_grid[-1, :])
    last_col_colors = np.unique(input_grid[:, -1])
    print(f"  Last Row Colors (Input): {last_row_colors}")
    print(f"  Last Column Colors (Input): {last_col_colors}")

examples = [
    ([[1, 8, 5, 1], [1, 5, 5, 1], [1, 5, 1, 1], [1, 1, 1, 1]], [[1, 8, 5], [1, 5, 5], [1, 5, 1]]),
    ([[1, 1, 1, 1, 2, 3, 4, 1], [1, 6, 1, 1, 1, 1, 1, 1], [1, 7, 8, 1, 9, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1]], [[1, 1, 1, 1, 2, 3, 4], [1, 6, 1, 1, 1, 1, 1], [1, 7, 8, 1, 9, 1, 1]]),
    ([[0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 1], [1, 1, 1, 1, 1, 1, 1]], [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]])
]

for i, (input_grid, output_grid) in enumerate(examples):
    print(f"Example {i+1}:")
    analyze_example(input_grid, output_grid)
