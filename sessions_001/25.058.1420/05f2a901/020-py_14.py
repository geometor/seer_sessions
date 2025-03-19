"""
1.  **Identify Objects:** Find the azure object (color 8) and the red object (color 2) within the input grid. If either object is not found, the input grid will be returned as is.
2.  **Determine New Position:** The red object's new position will be directly below the azure object.
3.  **Excise and stack:** The area between the bottom of azure and up to, but not including, red object should be removed. The area at and below red object to the bottom of the input show also be removed.
4.  **Construct Output:** Create a new grid where the azure object remains in its original position, and the red object is placed immediately below it, with other part of the grid are removed.
"""

import numpy as np

def find_object(grid, color):
    # Find the coordinates of all pixels of the specified color.
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return None, None, None, None
    # Determine the bounding box.
    min_row, min_col = coords.min(axis=0)
    max_row, max_col = coords.max(axis=0)
    return min_row, min_col, max_row, max_col

def transform(input_grid):
    # Initialize the output grid.  We'll modify this.
    output_grid = np.copy(input_grid)

    # Find the azure (8) object
    azure_min_row, _, azure_max_row, _ = find_object(input_grid, 8)

    # Find the red object (2)
    red_min_row, red_min_col, red_max_row, red_max_col = find_object(input_grid, 2)
    
    if azure_min_row is None or red_min_row is None:
        return input_grid
    
    # Calculate new height
    new_height = azure_max_row + 1 + (red_max_row - red_min_row + 1)
    output_grid = np.zeros((new_height, input_grid.shape[1]), dtype=int)

    # Copy azure object
    output_grid[:azure_max_row + 1, :] = input_grid[:azure_max_row + 1, :]

    # Copy red object
    row_shift = azure_max_row + 1
    for r in range(red_min_row, red_max_row + 1):
        for c in range(red_min_col, red_max_col + 1):
            output_grid[r - red_min_row + row_shift, c] = input_grid[r,c]

    return output_grid