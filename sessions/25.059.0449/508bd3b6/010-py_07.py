"""
The transformation rule takes each azure pixel and expands it into an "L" shape of green pixels to the right and down, stopping when there is no available cell, or they are out of the grid. The red block at the bottom remains unchanged.
"""

import numpy as np

def find_pixels_by_color(grid, color):
    """Finds the coordinates of all pixels of a specific color."""
    return np.argwhere(grid == color).tolist()

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    output_grid = np.copy(input_grid)
    azure_pixels = find_pixels_by_color(input_grid, 8)

    for row, col in azure_pixels:
        # Generate green pixel to the right
        if col + 1 < output_grid.shape[1] and output_grid[row, col + 1] == 0:
            output_grid[row, col + 1] = 3

        # Generate green pixels downwards
        current_row = row + 1
        current_col = col
        
        if current_row < output_grid.shape[0] and output_grid[current_row,current_col ] == 0:
            output_grid[current_row,current_col] = 3

        
        current_col = col +1
        while current_row < output_grid.shape[0] :

            if current_col < output_grid.shape[1] and output_grid[current_row,current_col] == 0:

                output_grid[current_row, current_col] = 3
                current_col +=1
            else:
                break
            current_row += 1
    return output_grid