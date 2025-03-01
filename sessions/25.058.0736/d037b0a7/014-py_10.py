"""
The transformation replicates the yellow pixel (value 4) at the top-left corner (0,0) downwards to fill the entire first column.
It also replicates the red pixel (value 2) at the center (1,1) downwards once. The white pixels (value 0) remain unchanged.
"""

import numpy as np

def get_pixel_by_value(grid, value):
    """Finds the first occurrence of a pixel with a specific value."""
    coords = np.where(grid == value)
    if len(coords[0]) > 0:
        return (coords[0][0], coords[1][0])  # Return row, col
    return None

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""
    output_grid = np.copy(input_grid)
    
    # Find yellow (4) and red (2) pixels
    yellow_pos = get_pixel_by_value(input_grid, 4)
    red_pos = get_pixel_by_value(input_grid, 2)
    
    if yellow_pos:
        # Replicate yellow downwards
        for row in range(yellow_pos[0], output_grid.shape[0]):
            output_grid[row, yellow_pos[1]] = 4
    
    if red_pos:
      # replicate one below original red
      output_grid[red_pos[0]+1, red_pos[1]] = 2
            
    return output_grid