"""
Replicates objects from the input grid to the output grid, maintaining their original colors, shapes, and positions. 
The second red object (reading top to bottom, left to right) generates a 1x3 vertical line of blue pixels one row below and one col to the left of its original position.
"""

import numpy as np

def find_objects(grid, color=None):
    objects = []
    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            if color is None or grid[y, x] == color:
                objects.append((x, y))
    return objects

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)

    # Find the second red object
    red_objects = find_objects(input_grid, color=2)
    if len(red_objects) >= 2:
        second_red_x, second_red_y = red_objects[1]

        # Create the blue line
        output_grid[second_red_y, second_red_x - 1] = 1
        output_grid[second_red_y + 1, second_red_x - 1] = 1
        output_grid[second_red_y + 1, second_red_x - 2] = 1

    return output_grid