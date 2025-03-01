"""
1.  **Locate:** Find the single yellow (4) pixel in the input grid.
2.  **Propagate:** From the initial yellow pixel location, draw a vertical line downwards to the bottom of the grid, copying the yellow pixel at each row.
3.  **Mirror Column:** Create a vertical line of yellow pixels one column to the right of the *original* yellow pixel location, mirroring the column created in step 2. This mirror happens only if the pixel to the right of the original location is white (0).
"""

import numpy as np

def find_pixel(grid, color):
    # Find the coordinates of a pixel of the specified color.
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] == color:
                return (i, j)
    return None

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)
    
    # Find the yellow pixel (4)
    yellow_pixel_coords = find_pixel(input_grid, 4)
    
    if yellow_pixel_coords:
        y, x = yellow_pixel_coords

        # Propagate downwards, copying the yellow pixel
        for i in range(output_grid.shape[0]):
            output_grid[i, x] = 4  # Yellow
        
        # Mirror column, check bounds and if the original neighbor was 0.
        if (x + 1) < output_grid.shape[1] and input_grid[y, x+1] == 0:
            for i in range(output_grid.shape[0]):
                output_grid[i, x + 1] = 4

    return output_grid