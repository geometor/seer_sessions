"""
Transforms an input grid by expanding azure regions from specified seed points and filling to the right,
constrained by red boundaries and grid edges.
"""

import numpy as np

def find_object(grid, color):
    # Find coordinates of pixels with the specified color.
    return np.argwhere(grid == color)

def transform(input_grid):
    # Initialize output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Find the red (2) pixels on the left.
    red_pixels_left = find_object(input_grid, 2)
    # Find the red (2) pixels on the right.
    red_pixels_right = find_object(input_grid, 2)
    
    # Find azure (8) pixels.
    azure_pixels = find_object(input_grid, 8)

    # 2. Upper Azure Expansion
    for ax, ay in azure_pixels:
        if any(ax == rx and ay > ry for rx, ry in red_pixels_left): # check to see if the azure pixel is "within" the left red region
             for j in range(ay + 1, width):
                if output_grid[ax, j] == 2:  # stop at red or edge
                    break
                output_grid[ax, j] = 8
                
    # 3. Lower Azure Expansion.
    for ax, ay in azure_pixels:
        if any(ax == rx and ay < ry for rx, ry in red_pixels_right):  #check to see if the azure pixel is "within" the right red region
             for j in range(ay - 1, -1, -1): # move to the left
                if output_grid[ax, j] == 2: # stop at red or edge
                    break
                output_grid[ax, j] = 8
    
    
    # Find yellow (4) pixels
    yellow_pixels = find_object(input_grid, 4)
        
    # 4. Replacement
    for yx, yy in yellow_pixels:
          for j in range(yy + 1, width):
            if output_grid[yx,j] == 8:
                output_grid[yx,j] = 4
                break # only the first to the right


    return output_grid