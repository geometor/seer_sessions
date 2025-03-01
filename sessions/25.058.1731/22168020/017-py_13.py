import numpy as np

def check_colors(grids):
    """Checks if only colors 6 and 8 are present and reports."""
    color_check_results = []
    for i, grid in enumerate(grids):
        unique_colors = np.unique(grid)
        is_valid = np.array_equal(np.sort(unique_colors[unique_colors != 0]), np.array([6, 8]))
        color_check_results.append(f"Example {i+1}: {'Pass' if is_valid else 'Fail'}")
    return color_check_results

def check_rows(grids):
    results = []

    for i, grid in enumerate(grids):
        valid = True
        for row in range(grid.shape[0]):
          unique = np.unique(grid[row])
          if len(unique) > 1:
            valid = False
        results.append(f"Example {i+1}: {'Pass' if valid else 'Fail'}")
    return results

# Example grids from the transform function execution results.
example_grids_output = [
    np.array([[6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 8, 8, 8, 8, 8, 8, 8, 8],
              [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 8, 8, 8, 8, 8, 8, 8, 8],
              [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 8, 8, 8, 8, 8, 8, 8, 8],
              [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 8, 8, 8, 8, 8, 8, 8, 8],
              [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 8, 8, 8, 8, 8, 8, 8, 8],
              [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 8, 8, 8, 8, 8, 8, 8, 8]]),
    np.array([[6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
              [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
              [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
              [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]]),
    np.array([[6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
              [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
              [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
              [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]]),
]
color_check_results = check_colors(example_grids_output)
print(f"Color Check Results: {color_check_results}")

row_check_results = check_rows(example_grids_output)
print(f"Row Check Results: {row_check_results}")