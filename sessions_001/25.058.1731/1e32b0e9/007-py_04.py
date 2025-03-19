import numpy as np

def grid_diff(grid1, grid2):
    """Counts the number of differing pixels between two grids."""
    return np.sum(grid1 != grid2)

def grid_report(grid):
    unique, counts = np.unique(grid, return_counts=True)
    color_counts = dict(zip(unique, counts))
    print(f"Dimensions: {grid.shape}")
    print(f"Color Counts: {color_counts}")

input_grid = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 8, 0, 0, 0, 0], [0, 0, 0, 0, 8, 0, 0, 0, 0], [0, 0, 0, 0, 8, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]])
expected_output = np.array([[0, 0, 0, 0, 8, 0, 0, 0, 0], [0, 0, 0, 0, 8, 0, 0, 0, 0], [0, 0, 0, 0, 8, 0, 0, 0, 0], [0, 0, 0, 0, 8, 0, 0, 0, 0], [0, 0, 0, 0, 8, 0, 0, 0, 0], [0, 0, 0, 0, 8, 0, 0, 0, 0], [0, 0, 0, 0, 8, 0, 0, 0, 0]])
actual_output = transform(input_grid)

print("Input Grid:")
grid_report(input_grid)
print("\nExpected Output Grid:")
grid_report(expected_output)
print("\nActual Output Grid:")
grid_report(actual_output)
print("\nDifference between Expected and Actual:")
print(grid_diff(expected_output, actual_output))
