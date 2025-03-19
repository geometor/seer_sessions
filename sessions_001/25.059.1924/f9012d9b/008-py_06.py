"""
1. Identify the Bottom Object: Examine the input grid and identify the rightmost object that has one or more pixels touching the bottom edge of the grid. It could be a single pixel or a larger shape.
2. Determine the Object's Color: Note the color value of the identified object.
3. Create Output Grid: Create a 2x2 output grid filled with white (color 0).
4. Set Bottom-Right Pixel: Set the color of the bottom-right pixel (at index [1, 1]) of the output grid to the color of the identified object.
5. Return Output Grid: Return the created 2x2 output grid.
"""

import numpy as np

def get_bottom_object_color(grid):
    """
    Finds the color of a bottom object in the grid.
    Returns the color of the object or 0 if no such object exists.
    """
    rows, cols = grid.shape
    for j in range(cols - 1, -1, -1):  # Iterate columns from right to left
        if grid[rows-1, j] != 0:
            return grid[rows-1, j]
    return 0

def transform(input_grid):
    # Create a 2x2 output grid filled with white
    output_grid = np.zeros((2, 2), dtype=int)

    # Find the color of the rightmost object on the bottom row.
    bottom_object_color = get_bottom_object_color(input_grid)
    
    # Set the bottom-right cell to the object's color
    output_grid[1, 1] = bottom_object_color

    return output_grid