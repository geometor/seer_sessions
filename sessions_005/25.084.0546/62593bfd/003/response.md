```python
"""
The transformation rule involves identifying all distinct, contiguous regions of non-black (non-0)
and non-grey (non-5) pixels, each considered an "object."  These objects are then stacked row-wise
in the output grid, starting from the top row (row 0).  The order of stacking is determined by
reading the input grid in *reverse* row order (bottom to top). Within each row band,
the objects' original horizontal (column) positions are preserved.
"""

import numpy as np

def find_objects(grid):
    """
    Finds contiguous objects (same color pixels) in a grid, excluding 0 and 5.

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of objects, where each object is a list of (row, col) tuples.
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
            if (row, col) not in visited and grid[row,col] != 0 and grid[row, col] != 5:
                current_object = []
                dfs(row, col, grid[row, col], current_object)
                objects.append(current_object)
    return objects

def transform(input_grid):
    """
    Transforms the input grid by stacking objects row-wise from bottom to top.
    """
    input_grid = np.array(input_grid)
    output_grid = np.full(input_grid.shape, input_grid[0,0])  # Initialize with background color from input

    # Find objects, excluding background (0 and 5)
    objects = find_objects(input_grid)

    # Sort objects by their *maximum* row index in *descending* order (bottom to top)
    objects.sort(key=lambda obj: max(row for row, _ in obj), reverse=True)

    current_row = 0
    for obj in objects:
        # Find the height of this object
        min_obj_row = min(row for row, _ in obj)
        max_obj_row = max(row for row, _ in obj)
        obj_height = max_obj_row - min_obj_row + 1

        # Place the object in the output grid, preserving original column positions
        for row, col in obj:
            output_grid[current_row + row - min_obj_row , col] = input_grid[row, col]

        current_row += obj_height  # Move to the next available row band

    return output_grid.tolist()
```