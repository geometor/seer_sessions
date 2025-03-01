import numpy as np

def analyze_example(input_grid, output_grid):
    """Analyzes the input and output grids for dimensions and cross properties."""

    input_rows, input_cols = input_grid.shape
    output_rows, output_cols = output_grid.shape

    dimensions_match = (input_rows == output_rows) and (input_cols == output_cols)

    # Find where the output grid is not 0 (white)
    non_zero_indices = np.argwhere(output_grid != 0)
    if len(non_zero_indices) > 0:
        center_row = non_zero_indices[0][0]
        is_horizontal = all(x[0] == center_row for x in non_zero_indices)
        center_col = non_zero_indices[0][1]
        is_vertical = all(x[1] == center_col for x in non_zero_indices)
    else:
        center_row = -1
        center_col = -1
        is_horizontal = False
        is_vertical = False

    cross_row = -1
    cross_col = -1
    horizontal_found = False
    vertical_found = False

    # Check for cross shape
    if dimensions_match:
        # Check for Horizontal Line
        for r in range(output_rows):
            if all(output_grid[r,c] != 0 for c in range(output_cols)):
                horizontal_found = True
                cross_row = r
                break
        for c in range(output_cols):
            if all(output_grid[r,c] != 0 for r in range(output_rows)):
                vertical_found = True
                cross_col = c
                break

    cross_present = horizontal_found and vertical_found

    return {
        "dimensions_match": dimensions_match,
        "output_rows": output_rows,
        "output_cols": output_cols,
        "cross_present": cross_present,
        "cross_row": cross_row,
        "cross_col": cross_col
    }

# Dummy data for demonstration - replace with actual task data
examples = [
    (np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]]), np.array([[0, 0, 0], [0, 8, 0], [0, 0, 0]])),  # Example 1 (modified for demo)
    (np.array([[0, 0, 0], [0, 0, 0], [0, 8, 0]]), np.array([[0, 8, 0], [0, 8, 0], [0, 8, 0]])),  # Example 2 (modified for demo)
    (np.array([[9, 9, 9], [9, 9, 9], [9, 9, 9]]), np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])),  # Example 3 (modified for demo)
]
results = []
for input_grid, output_grid in examples:
     results.append(analyze_example(input_grid, output_grid))

print(results)
