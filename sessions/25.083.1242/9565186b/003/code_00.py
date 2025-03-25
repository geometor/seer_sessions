"""
Iterates through each cell in the input grid. If the cell's color is 1, 2, 3, or 8,
AND if not all cells in that row have the same color value, the cell's value in
the output grid is changed to 5. Otherwise, the input cell color is copied to
the output grid. Returns the modified grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    
    # Get the dimensions of the grid
    rows, cols = input_grid.shape

    # Iterate through each cell of the input grid
    for i in range(rows):
        # Check if all cells in the current row have the same value
        row_values = input_grid[i, :]
        all_same_color = np.all(row_values == row_values[0])

        for j in range(cols):
            # Check the color value of the cell
            if input_grid[i, j] in [1, 2, 3, 8] and not all_same_color:
                # Replace the cell's value in the output grid with 5 (gray)
                output_grid[i, j] = 5
            # Else, the color remains the same (copy performed during initialization)

    # Return the modified grid as the output
    return output_grid