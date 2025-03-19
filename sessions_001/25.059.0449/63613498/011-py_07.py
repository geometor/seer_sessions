import numpy as np

# Example from the training data (let's take the first one)
input_grid = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 5, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 6, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
])

expected_output_grid = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 5, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 5, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
])

# Previous Code generated transform function
def transform(input_grid):
    output_grid = np.copy(input_grid)
    output_grid[output_grid == 6] = 5
    return output_grid

actual_output_grid = transform(input_grid)

# Check if the actual output matches the expected output
are_grids_equal = np.array_equal(actual_output_grid, expected_output_grid)
print(f"Grids are equal: {are_grids_equal}")

# Count magenta pixels in input
magenta_pixels_input = np.sum(input_grid == 6)
print(f"Magenta Pixels in Input: {magenta_pixels_input}")

# Count grey pixels in input
grey_pixels_input = np.sum(input_grid == 5)
print(f"Grey Pixels in Input: {grey_pixels_input}")

# Count magenta pixels in output
magenta_pixels_output = np.sum(expected_output_grid == 6)
print(f"Magenta Pixels in Output: {magenta_pixels_output}")

# Count grey pixels in output
grey_pixels_output = np.sum(expected_output_grid == 5)
print(f"Grey Pixels in Output: {grey_pixels_output}")
