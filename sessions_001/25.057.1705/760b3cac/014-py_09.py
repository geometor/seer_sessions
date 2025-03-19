"""
Copies shape 8 to its adjacent left and removes the original shape 8. Shape 4 remains the same.
"""

import numpy as np

def find_objects(grid, color):
    # Find coordinates of all pixels of the specified color.
    coords = np.argwhere(grid == color)
    return coords.tolist()

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Find objects of color 8 (azure) and 4 (yellow)
    azure_objects = find_objects(input_grid, 8)
    yellow_objects = find_objects(input_grid, 4)
    
    # Remove the original azure shape
    for x, y in azure_objects:
      output_grid[x,y] = 0

    # Yellow shape remains the same (already copied during initialization)

    # Mirror and duplicate azure shape.
    for x, y in azure_objects:
        new_x = x
        new_y = y - 2 # shift to the adjacent left by 2 pixels to create a mirror effect
        if 0 <= new_x < output_grid.shape[0] and 0 <= new_y < output_grid.shape[1]:
             output_grid[new_x,new_y]= 8
        new_y = y - 1
        if 0 <= new_x < output_grid.shape[0] and 0 <= new_y < output_grid.shape[1]:
            output_grid[new_x,new_y] = 8

    return output_grid