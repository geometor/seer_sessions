"""
Examine the input grid. Consider contiguous blocks of pixels with the same color as "objects".
Any object that is colored Green or Yellow is transformed to Magenta. Create a new grid where
identified objects are transformed, all other pixels retain their original color from the input grid.
"""

import numpy as np

def find_objects(grid):
    """
    Identify contiguous blocks of pixels with the same color as objects.
    Returns a list of objects, where each object is a list of (row, col) coordinates.
    """
    visited = set()
    objects = []

    def dfs(row, col, color, current_object):
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
            return
        visited.add((row, col))
        current_object.append((row, col))
        dfs(row + 1, col, color, current_object)
        dfs(row - 1, col, color, current_object)
        dfs(row, col + 1, color, current_object)
        dfs(row, col - 1, color, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if (row, col) not in visited:
                current_object = []
                dfs(row, col, grid[row, col], current_object)
                if current_object:
                    objects.append(current_object)
    return objects

def transform(input_grid):
    # initialize output_grid as a copy of input
    output_grid = np.copy(input_grid)

    # Find all objects in the input grid
    objects = find_objects(input_grid)

    # Iterate through each object
    for obj in objects:
        # Get the color of the object (assuming all pixels in the object have the same color)
        if obj:  # Make sure the object isn't empty
           first_pixel_row, first_pixel_col = obj[0]
           object_color = input_grid[first_pixel_row, first_pixel_col]

           # Transform the object to magenta if it's green or yellow
           if object_color == 3 or object_color == 4:
               for row, col in obj:
                   output_grid[row, col] = 6

    return output_grid