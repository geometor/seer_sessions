"""
The transformation rule involves identifying contiguous blocks of non-zero colored pixels (objects) in the input grid.
For each object, the last two columns are duplicated and shifted one column to the right.
The background (0-colored pixels) is preserved.
"""

import numpy as np

def get_objects(grid):
    """
    Identifies and returns a list of objects in the grid.
    Each object is represented by a list of (row, col) coordinates.
    """
    objects = []
    visited = set()
    rows, cols = grid.shape
    
    def dfs(row, col, current_object):
        if (row, col) in visited or not (0 <= row < rows and 0 <= col < cols) or grid[row, col] == 0:
            return
        visited.add((row, col))
        current_object.append((row, col))
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and (r, c) not in visited:
                current_object = []
                dfs(r, c, current_object)
                objects.append((grid[r,c],current_object)) # save value with the object
    return objects

def transform(input_grid):
    """
    Transforms the input grid according to the rule: duplicate and shift the last two columns of each object one column to the right.
    """
    output_grid = np.copy(input_grid)
    objects = get_objects(input_grid)

    for color, obj in objects:
        # Find the columns present in the object
        columns = sorted(list(set(col for _, col in obj)))

        # Handle edge case: object has fewer than 2 columns
        if len(columns) < 2:
            columns_to_duplicate = columns # duplicate available
        else:
            columns_to_duplicate = columns[-2:] # Get the last two columns

        # Duplicate and shift these columns
        for row, col in obj:
            if col in columns_to_duplicate:
                if col + 1 < output_grid.shape[1]:
                    output_grid[row, col + 1] = input_grid[row,col]
    return output_grid