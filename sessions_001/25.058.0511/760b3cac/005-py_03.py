"""
1.  **Identify:** Find all azure (8) and yellow (4) pixels in the input grid.
2.  **Preserve Yellow:** Maintain the positions of the yellow pixels, meaning if a row or column in the input grid has some yellow pixels, it is identical in the output grid
3.  **Reposition Azure:** For each column containing azure pixels in the input, copy it, without shifting, to the same x position at the top-most available row. If yellow occupies any of the rows, then stack azure above or below depending on the relative position of yellow to the original azure, but always on the same x (column) position.
"""

import numpy as np

def find_pixels(grid, color):
    return np.argwhere(grid == color)

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    
    # Find all azure and yellow pixels
    azure_pixels = find_pixels(input_grid, 8)
    yellow_pixels = find_pixels(input_grid, 4)

    # Preserve Yellow Pixels: Copy yellow pixels directly to the output grid.
    for y, x in yellow_pixels:
        output_grid[y, x] = 4

    # Reposition Azure Pixels
    for y, x in azure_pixels:
        # Find the top-most available row in the same column
        new_y = 0
        while new_y < input_grid.shape[0] and output_grid[new_y, x] != 0 and output_grid[new_y,x] != 8:
            
            new_y += 1
            
        # place azure
        output_grid[new_y, x] = 8
    

    return output_grid