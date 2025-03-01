# ef135b50 • 010 • example_2 • investigate_coder

---
```python
"""
Identify regions of red (2) pixels. Change the color of some red (2) pixels to
maroon (9) to fill gaps and make the red regions more rectangular.
"""

import numpy as np

def get_objects(grid, color):
    """
    Find connected regions of a specific color.
    Returns a list of sets, where each set contains the (row, col) coordinates of a connected region.
    """
    visited = set()
    objects = []

    def dfs(row, col, current_object):
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or (row, col) in visited
            or grid[row, col] != color
        ):
            return
        visited.add((row, col))
        current_object.add((row, col))
        # Check adjacent cells (up, down, left, right)
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and (row, col) not in visited:
                current_object = set()
                dfs(row, col, current_object)
                objects.append(current_object)
    return objects

def is_enclosed(grid, row, col, target_color):
    """Check if a cell is fully surrounded by target color (including diagonals)"""
    for r in range(max(0, row -1), min(grid.shape[0], row + 2)):
        for c in range(max(0, col - 1), min(grid.shape[1], col + 2)):
            if grid[r,c] != target_color:
                return False
    return True

def fill_gaps(grid, red_objects):
    """
    Fill concave gaps in connected red areas, changes to maroon color.
    """
    output_grid = np.copy(grid)

    for obj in red_objects:

        #convert the sets of tuples in obj to a 2-D array
        rows, cols = zip(*obj) #Unpacks set of tuples into two tuples of x and y coordinates
        min_row, max_row = min(rows), max(rows)
        min_col, max_col = min(cols), max(cols)

        #fills any gaps found
        for r in range(min_row, max_row + 1):
             for c in range(min_col, max_col + 1):
                 if output_grid[r,c]==2:
                  output_grid[r,c] = 9

    return output_grid

def transform(input_grid):
    # Initialize output grid
    output_grid = np.copy(input_grid)

    # Find red objects
    red_objects = get_objects(input_grid, 2)

    # Fill concave gaps
    output_grid = fill_gaps(output_grid, red_objects)

    return output_grid
```
