"""
Identify gray rectangles and change the color of the inner gray pixels to red, 
leaving a one-pixel wide gray border.
"""

import numpy as np

def find_objects(grid, color):
    # Find contiguous blocks of a given color.  This function does not enforce
    # that they are rectangular, the caller must do that if needed.
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(r, c, current_object):
        if (r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or
                visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        current_object.append((r, c))
        dfs(r + 1, c, current_object)
        dfs(r - 1, c, current_object)
        dfs(r, c + 1, current_object)
        dfs(r, c - 1, current_object)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if not visited[r, c] and grid[r, c] == color:
                current_object = []
                dfs(r, c, current_object)
                objects.append(current_object)
    return objects

def is_rectangle(obj, grid):
    # basic rectangle check
    if not obj:
        return False

    rows = [r for r, _ in obj]
    cols = [c for _, c in obj]
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)

    expected_size = (max_row - min_row + 1) * (max_col - min_col + 1)
    return len(obj) == expected_size

def get_inner_pixels(obj):
    # returns the inner pixels of the object
    rows = [r for r, _ in obj]
    cols = [c for _, c in obj]
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)

    inner_pixels = []
    for r, c in obj:
        if min_row < r < max_row and min_col < c < max_col:
            inner_pixels.append((r,c))

    return inner_pixels
    
def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Find gray rectangles
    gray_objects = find_objects(input_grid, 5)
    gray_rectangles = [obj for obj in gray_objects if is_rectangle(obj, input_grid)]
    
    # Iterate through each gray rectangle
    for rect in gray_rectangles:
        #get inner pixels
        inner_pixels = get_inner_pixels(rect)

        # change color of inner pixels
        for r, c in inner_pixels:
            output_grid[r, c] = 2
    
    return output_grid