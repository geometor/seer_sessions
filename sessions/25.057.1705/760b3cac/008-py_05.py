"""
Identifies an azure (8) object and a yellow (4) object within a grid. 
The azure object is expanded to the right. 
If two horizontally adjacent azure pixels have a white pixel to their right, the white pixel is changed to azure.
The yellow object remains unchanged.
"""

import numpy as np

def find_objects(grid):
    """
    Finds contiguous blocks of pixels with the same color.
    Returns a dictionary of objects, keyed by color.
    """
    objects = {}
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, obj_pixels):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        obj_pixels.append((row, col))
        dfs(row + 1, col, color, obj_pixels)
        dfs(row - 1, col, color, obj_pixels)
        dfs(row, col + 1, color, obj_pixels)
        dfs(row, col - 1, color, obj_pixels)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col]:
                color = grid[row, col]
                obj_pixels = []
                dfs(row, col, color, obj_pixels)
                if color not in objects:
                    objects[color] = []
                objects[color].append(obj_pixels)
    return objects

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)

    # Find objects in the input grid
    objects = find_objects(input_grid)

    # Check if azure (8) exists in the objects
    if 8 not in objects:
        return output_grid

    # Iterate through each azure object
    for azure_object in objects[8]:
        # Create a set for quick pixel lookup
        azure_pixels = set(azure_object)
        
        # Iterate through the azure pixels to find pairs and apply fill rule
        for row, col in azure_pixels:
            #check for pairs
            if (row, col + 1) in azure_pixels:
                #check for white to the right
                if col + 2 < output_grid.shape[1] and output_grid[row, col + 2] == 0:
                    output_grid[row, col + 2] = 8
            

    return output_grid