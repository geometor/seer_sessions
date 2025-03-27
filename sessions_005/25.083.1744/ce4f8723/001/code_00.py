"""
1.  **Identify Input Sections:** Divide the input into two grids, using the row "4 4 4 4" as the delimiter. Consider only top grid as the *active* section.
2.  **Iterate:** For each cell in the *active* input grid:
    *   If the cell value is `1`, change it to `3` in the corresponding cell of the output grid.
    *   If the cell value is `0`, keep it as `0` in the output grid.
3. Ignore the lower input grid.
"""

import numpy as np

def find_delimiter_row(grid, delimiter_value=4):
    """Finds the row index that acts as a delimiter."""
    for i, row in enumerate(grid):
        if np.all(row == delimiter_value):
            return i
    return -1  # Or some other indicator that the delimiter isn't found

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""
    # Convert input_grid to a NumPy array for easier manipulation.
    grid = np.array(input_grid)
    
    # Find row that contains all 4s
    delimiter_row_index = find_delimiter_row(grid)
    
    # Separate grids
    top_grid = grid[:delimiter_row_index]
    
    # Initialize output_grid.
    output_grid = np.zeros_like(top_grid)
    
    # Iterate through the *top* input grid
    for i in range(top_grid.shape[0]):
        for j in range(top_grid.shape[1]):
            if top_grid[i, j] == 1:
                output_grid[i, j] = 3
            else:
                output_grid[i,j] = top_grid[i,j]

    return output_grid.tolist()