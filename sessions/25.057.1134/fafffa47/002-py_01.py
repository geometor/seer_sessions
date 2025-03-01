"""
1.  **Identify** the maroon (9) object within the input grid.
2.  **Extract** the top two rows.
3.   **Change** maroon color (value 9) to red (value 2)
4.   Fill remaining area of the output grid with white (value 0).
"""

import numpy as np

def find_object(grid, color):
    # Find the coordinates of all cells with the specified color.
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return None, None, None, None  # Return None if color not found
    min_row = coords[:, 0].min()
    max_row = coords[:, 0].max()
    min_col = coords[:, 1].min()
    max_col = coords[:, 1].max()
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((3, 3), dtype=int)

    # Find the maroon object (color 9).
    min_row, max_row, min_col, max_col = find_object(input_grid, 9)
    
    if min_row is not None:
        # Extract the top two rows of the maroon object and change color to red (2)
        for i in range(min_row, min(min_row + 2, max_row + 1)):
          for j in range(min_col, max_col + 1):
            if i - min_row < output_grid.shape[0] and j - min_col < output_grid.shape[1]:
                output_grid[i - min_row, j - min_col] = 2


    return output_grid