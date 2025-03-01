import numpy as np

# Helper function to get grid information
def grid_info(grid):
    azure_pixels = np.where(grid == 8)
    if azure_pixels[0].size > 0:
        azure_row, azure_col = azure_pixels[0][0], azure_pixels[1][0]
    else:
        azure_row, azure_col = None, None
    return {
        "shape": grid.shape,
        "azure_pixel_location": (azure_row, azure_col) if azure_row is not None else None,
    }

# Example grids (replace with actual grids from the task)
example1_input = np.array([
    [2, 2, 2, 2, 2],
    [2, 2, 8, 2, 2],
    [2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2]
])
example1_output = np.array([
    [2, 2, 2, 2, 2],
    [2, 2, 8, 2, 2],
    [2, 2, 8, 2, 2],
    [2, 2, 8, 2, 2],
    [2, 2, 8, 2, 2],
    [2, 2, 2, 2, 2]
])
example2_input = np.array([
    [2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 8, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2]
])
example2_output = np.array([
    [2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2],
    [2, 2, 2, 8, 2, 2, 2],
    [2, 2, 2, 2, 2, 2, 2]
])
example3_input = np.array([
    [2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2],
    [2, 2, 8, 2, 2],
    [2, 2, 2, 2, 2]
])
example3_output = np.array([
    [2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2],
    [2, 2, 2, 2, 2],
    [2, 2, 8, 2, 2],
    [2, 2, 8, 2, 2]
])

# Analyze the examples
examples = [
    (example1_input, example1_output),
    (example2_input, example2_output),
    (example3_input, example3_output),
]

for i, (input_grid, output_grid) in enumerate(examples):
    input_info = grid_info(input_grid)
    output_info = grid_info(output_grid)

    print(f"Example {i + 1}:")
    print(f"  Input: {input_info}")
    print(f"  Output: {output_info}")