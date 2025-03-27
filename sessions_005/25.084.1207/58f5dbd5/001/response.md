```python
"""
Identify the border color from the top-left pixel (0,0).
Find the index of the first row (H) that consists entirely of the border color.
Find the index of the first column (W) that consists entirely of the border color.
Crop the input grid to include all rows from 0 to H (inclusive) and all columns from 0 to W (inclusive).
"""

import numpy as np

def find_first_full_row(grid, color):
    """Finds the index of the first row entirely composed of the specified color."""
    num_rows, num_cols = grid.shape
    for r in range(num_rows):
        if np.all(grid[r, :] == color):
            return r
    return num_rows - 1 # Should not happen based on examples, but return last row index if no full row found

def find_first_full_column(grid, color):
    """Finds the index of the first column entirely composed of the specified color."""
    num_rows, num_cols = grid.shape
    for c in range(num_cols):
        if np.all(grid[:, c] == color):
            return c
    return num_cols - 1 # Should not happen based on examples, but return last col index if no full col found

def transform(input_grid):
    """
    Crops the input grid based on the first complete row and column 
    matching the border color (top-left pixel).
    """
    # Convert input list of lists to a numpy array for easier slicing and checking
    input_np = np.array(input_grid, dtype=int)

    # 1. Determine the border_color
    border_color = input_np[0, 0]

    # 2. Find the index (H) of the first row composed entirely of the border_color
    h_index = find_first_full_row(input_np, border_color)

    # 3. Find the index (W) of the first column composed entirely of the border_color
    w_index = find_first_full_column(input_np, border_color)

    # 4. Crop the input grid using the found indices
    # The slice includes the row/column at the index, hence +1
    output_grid = input_np[0:h_index + 1, 0:w_index + 1]

    # Convert back to list of lists if required by the environment
    return output_grid.tolist()

```