"""
The transformation rule involves swapping the colors of two inner, nested squares within a grid, while preserving the outermost border color.
"""

import numpy as np

def get_objects(grid):
    # Find the outermost border color
    border_color = grid[0, 0]
    
    # Find the next inner color
    for i in range(1, grid.shape[0] - 1):
        if grid[i,1] != border_color:
          inner_color1 = grid[i,1]
          break
    
    
    #Find center color
    center = grid.shape[0] // 2
    inner_color2 = grid[center, center]

    return border_color, inner_color1, inner_color2

def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    
    # Get border and inner square colors
    border_color, inner_color1, inner_color2 = get_objects(input_grid)

    # Iterate through the grid, excluding the outermost border
    for i in range(1, input_grid.shape[0] - 1):
        for j in range(1, input_grid.shape[1] - 1):
            # Swap colors inside the border
            if input_grid[i,j] == inner_color1:
              output_grid[i,j] = inner_color2
            elif input_grid[i, j] == inner_color2:
              output_grid[i,j] = inner_color1

    return output_grid