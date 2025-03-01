"""
1. Identify Red Objects: Find all contiguous regions (objects) of *red* pixels (color code 2) in the input grid.
2. Find Largest Red Object: Among the red objects, identify the one with the largest number of pixels.
3. Determine Bounding Box: Calculate the bounding box of this largest red object. The bounding box is defined by the top-left and bottom-right corner coordinates.
4. Create Green Square:  Place a 3x3 green square (color code 3) in the output grid. The top-left corner of this square should coincide with the top-left corner of the bounding box calculated in the previous step.
5. Set Background: Set all pixels in the output grid that are not part of the green square to white (color code 0).
"""

import numpy as np

def find_red_objects(grid):
    """Finds contiguous regions of red pixels (color code 2)."""
    red_objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, current_object):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != 2):
            return
        visited[row, col] = True
        current_object.append((row, col))
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if not visited[r, c] and grid[r, c] == 2:
                current_object = []
                dfs(r, c, current_object)
                red_objects.append(current_object)
    return red_objects

def bounding_box(object_pixels):
    """Calculates the bounding box of a set of pixels."""
    if not object_pixels:
        return None
    min_row = min(pixel[0] for pixel in object_pixels)
    max_row = max(pixel[0] for pixel in object_pixels)
    min_col = min(pixel[1] for pixel in object_pixels)
    max_col = max(pixel[1] for pixel in object_pixels)
    return (min_row, min_col), (max_row, max_col)

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)
    
    # Find red objects in the input grid
    red_objects = find_red_objects(input_grid)
    
    # Find largest red object by pixel count
    largest_red_object = max(red_objects, key=len, default=[])

    # determine the bounding box
    if largest_red_object:
        top_left, _ = bounding_box(largest_red_object)
        
        # Draw 3x3 green square based on bounding box start
        for i in range(3):
            for j in range(3):
                row = top_left[0] + i
                col = top_left[1] + j
                if 0 <= row < output_grid.shape[0] and 0 <= col < output_grid.shape[1]:
                    output_grid[row, col] = 3

    return output_grid