def describe_grid(grid, name="Grid"):
    rows, cols = grid.shape
    unique_colors = np.unique(grid)
    print(f"{name}:")
    print(f"  Shape: {rows}x{cols}")
    print(f"  Unique Colors: {unique_colors}")
    
import numpy as np
# Example usage (replace with actual grids)
input_grid = np.array([
    [1, 5, 3],
    [5, 2, 5],
    [1, 1, 5]
])
expected_output_grid = np.array([
    [1, 1, 3],
    [5, 2, 2],
    [1, 1, 5]
])
actual_output_grid = transform(input_grid.copy())
print(f"Matches Expected: {np.array_equal(actual_output_grid, expected_output_grid)}")
describe_grid(input_grid, "Input")
describe_grid(expected_output_grid, "Expected Output")
describe_grid(actual_output_grid, "Actual Output")
