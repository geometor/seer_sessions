"""
The transformation involves identifying static and moving parts of yellow objects based on overlap with blue objects. Non-overlapping yellow pixels remain static. Overlapping yellow pixels change to blue and move to a new, centered position at the bottom of the grid.
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

    # combine all yellow objects into one for easier handling
    yellow_object = []
    for obj in yellow_objects:
        yellow_object.extend(obj)

    # Find overlapping pixels between blue and yellow
    overlapping_pixels = find_overlapping_pixels(blue_object, yellow_object)

    # Separate Static and Moving Yellow, and copy static yellow pixels
    for r, c in yellow_object:
        if (r,c) not in overlapping_pixels:
            output_grid[r, c] = 4 # Static Yellow
        
    # Calculate center offset for the bottom
    if overlapping_pixels:
        min_r = min(r for r, c in overlapping_pixels)
        max_r = max(r for r, c in overlapping_pixels)        
        height = max_r - min_r + 1
        bottom_center_row = input_grid.shape[0] - (height+1)
        row_offset = bottom_center_row - min_r

    # Move overlapping blue pixels, replacing the yellow
    for r, c in overlapping_pixels:
        new_r = r + row_offset
        output_grid[new_r, c] = 1


    return output_grid