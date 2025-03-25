"""
The transformation rule identifies distinct contiguous blocks of non-zero (non-white) colored pixels in the input grid and consolidates them horizontally while preserving their vertical positions and shapes. Blocks of the same color that are not adjacent are treated as separate objects. The objects are placed adjacent to each other from left to right in the output grid, based on their original horizontal positions.  The vertical position is determined by considering a combined, 2-row bounding box.
"""

import numpy as np

def get_distinct_objects(grid):
    """
    Finds all distinct contiguous blocks of non-zero pixels in the grid.
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, obj):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        obj.append((row, col))
        dfs(row + 1, col, color, obj)
        dfs(row - 1, col, color, obj)
        dfs(row, col + 1, color, obj)
        dfs(row, col - 1, color, obj)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] != 0 and not visited[row, col]:
                obj = []
                dfs(row, col, grid[row, col], obj)
                objects.append((grid[row, col], obj))  # Store color and object pixels
    return objects

def transform(input_grid):
    # Initialize output_grid as a zero-filled grid
    output_grid = np.zeros_like(input_grid)

    # Get distinct objects from the input grid
    objects = get_distinct_objects(input_grid)

    # Sort objects by their leftmost pixel's column (min_col)
    objects_sorted = sorted(objects, key=lambda x: min(p[1] for p in x[1]))

    # Consolidate and place objects horizontally
    next_col = 0  # Track the next available column in the output
    occupied_rows = set() #track rows used

    for color, obj_pixels in objects_sorted:
        # Get object's bounding box information
        rows, cols = zip(*obj_pixels)
        min_row = min(rows)
        max_row = max(rows)
        #min_col = min(cols) #not needed
        height = max_row - min_row + 1
        width = max(cols) - min(cols) + 1

        #find rows for object
        target_row = min_row
        
        # Copy the object into the output grid
        for r_offset in range(height):
            for c_offset in range(width):
                output_grid[target_row + r_offset, next_col + c_offset] = color
                
        #update occupied rows and next available col
        next_col += width

    return output_grid