"""
The transformation rule involves extracting a 4x4 sub-grid from the top-left corner of the input grid. 
Then, iterate through the input sub-grid using a 2x2 window. 
Within the 2x2 sub-grid, if it's not mixed color, meaning the output pixel is 3.
Otherwise, output pixel is 0.
"""

import numpy as np

def transform(input_grid):
    input_grid = np.array(input_grid)
    output_height = 4
    output_width = 4
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through the input sub-grid with a 2x2 window
    for i in range(output_height):
        for j in range(output_width):
            # Extract 2x2 sub-grid
            sub_grid = input_grid[i:i+2, j:j+2]
            
            # Check if the sub-grid contains only one color and not all are white (0)
            unique_colors = np.unique(sub_grid)
            if len(unique_colors) == 1 and unique_colors[0] != 0 :
              output_grid[i, j] = 3
            else:
              output_grid[i,j] = 0
    
    return output_grid.tolist()