"""
The transformation involves identifying yellow objects and blue objects. Yellow pixels that overlap with blue pixels are removed. Where the yellow object was, is replaced with a blue object. Yellow pixels that don't overlap remain unchanged.
"""

import numpy as np

def find_objects(grid, color):
    """Finds contiguous objects of a given color in the grid."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(r, c, obj):
        if (r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or
                visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        obj.append((r, c))
        dfs(r + 1, c, obj)
        dfs(r - 1, c, obj)
        dfs(r, c + 1, obj)
        dfs(r, c - 1, obj)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color and not visited[r, c]:
                obj = []
                dfs(r, c, obj)
                objects.append(obj)
    return objects

def find_overlapping_pixels(obj1, obj2):
    """Finds the pixels where two objects overlap."""
    pixels1 = set(obj1)
    pixels2 = set(obj2)
    return list(pixels1.intersection(pixels2))

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # Find blue and yellow objects
    blue_objects = find_objects(input_grid, 1)
    yellow_objects = find_objects(input_grid, 4)
    
    # combine all blue objects into one object for easier handling
    blue_object = []
    for obj in blue_objects:
        blue_object.extend(obj)

    # Iterate through each yellow object separately.
    for yellow_object in yellow_objects:
        # Find overlapping pixels between the current yellow object and any blue object.
        overlapping_pixels = find_overlapping_pixels(yellow_object, blue_object)
        
        if overlapping_pixels:
            # If overlap, create a blue object at yellow's position.
            for r, c in yellow_object:
                output_grid[r,c] = 1
        else:
             # copy yellow object that has no overlaps
            for r, c in yellow_object:
                output_grid[r, c] = 4

    return output_grid