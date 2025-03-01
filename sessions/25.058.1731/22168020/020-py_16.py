"""
Transforms input grids based on the presence of magenta (6) and azure (8) colors, considering both row-wise and column-wise conditions.

1.  **Initialization:** Start with an output grid filled with zeros, having the same dimensions as the input grid.
2.  **Row Check:** For each row in the input grid:
    *   If the row contains magenta (6), fill the entire corresponding row in the *output* grid with magenta.
    *   Else, If the row contains azure (8), *and azure does not exist in every column of the input grid,* fill the entire corresponding row in the output grid with azure.
    *   Else (if neither magenta nor satisfies the condition), the output row is all zeros.
3.  **Column Check - Special Condition:** If *every* column in the input grid has at least one azure (8) pixel, then fill the *output* with all zeros.
"""

import numpy as np

def _azure_in_all_columns(grid):
    """Checks if every column in the grid contains at least one azure (8) pixel."""
    num_cols = grid.shape[1]
    for j in range(num_cols):
        if 8 not in grid[:, j]:
            return False
    return True

def transform(input_grid):
    # Initialize output grid with zeros
    output_grid = np.zeros_like(input_grid)

    # Column Check - Special Condition
    if _azure_in_all_columns(input_grid):
        return output_grid  # Return all zeros

    # Row Check
    for i in range(input_grid.shape[0]):
        row = input_grid[i, :]
        if 6 in row:
            output_grid[i, :] = 6
        elif 8 in row:
            output_grid[i, :] = 8

    return output_grid