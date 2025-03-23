"""
1. Copy the Input: Start with a copy of the input grid.
2. Iterate through Columns: For each column, starting from the leftmost column (index 0):
3. Propagate Non-Zero Values Downward: If a cell in the current column has a non-zero value, replace all cells below it in the *same* column with that value. This propagation continues to the bottom of the grid.
4. Iterate until completed: move to the next column and repeat until the last column.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid with a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each column
    for j in range(cols):
        # Iterate through each cell in the current column
        for i in range(rows):
            # If the current cell has a non-zero value
            if output_grid[i, j] != 0:
                # Propagate the value downwards
                for k in range(i + 1, rows):
                    output_grid[k, j] = output_grid[i, j]

    return output_grid