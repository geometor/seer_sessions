"""
1.  **Iterate through the grid:** Starting from the second row (index 1), examine each cell.
2.  **Conditional propagation:** For each cell, check if the cell directly *above* it in the previous row has a non-zero value.
3.  **Copy value:** If the cell above is non-zero, copy its value to the current cell.
4. **Leave Unchanged:** Otherwise (if above cell is 0), do not modify the cell.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Iterate through the grid, starting from the second row
    for r in range(1, rows):
        for c in range(cols):
            # Check if the cell above is non-zero
            if output_grid[r-1, c] != 0:
                # Copy the value from the cell above
                output_grid[r, c] = output_grid[r-1, c]

    return output_grid