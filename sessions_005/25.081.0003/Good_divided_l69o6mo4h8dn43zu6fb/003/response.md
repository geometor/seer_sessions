```python
"""
The transformation rule involves removing pixels of color 4 (yellow) and 2 (red) from the input grid, then filling the remaining spaces with the non-removed pixels by shifting them down within their respective columns, and finally, filling up any remaining empty cells with color 0 (white).
"""

import numpy as np

def transform(input_grid):
    # Create a copy of the input grid, converting to integers for easier manipulation.
    output_grid = np.copy(input_grid).astype(int)
    height = output_grid.shape[0]
    width = output_grid.shape[1]

    # 1. Identify and Remove (mark as -1)
    for i in range(height):
        for j in range(width):
            if output_grid[i, j] == 4 or output_grid[i, j] == 2:
                output_grid[i, j] = -1

    # 2. Fill Down and 3. Re-arrange
    for j in range(width):
        # Collect non-removed pixels for this column
        column_values = []
        for i in range(height):
            if output_grid[i, j] != -1:
                column_values.append(output_grid[i, j])

        # Fill the column from top to bottom with collected values.
        for i in range(height):
            if i < len(column_values):
                output_grid[i, j] = column_values[i]
            else:
                # 4. fill remaining spaces with 0
                output_grid[i,j] = 0

    return output_grid
```