```python
"""
1.  **Identify Blue Objects:** Scan the input grid and identify all distinct contiguous regions of '1' (blue) pixels. Consider pixels to be part of the same object if they are adjacent (up, down, left, or right - not diagonal).
2.  **Count Blue Objects:** Count the number of distinct blue objects identified.
3.  **Construct the beginning of output:** Create a new 1D array. For each distinct blue region, append `1` to array.
4.  **Construct the end of output:** Append one `0` to the output array.
5.  **Return:** output the array
"""

import numpy as np

def find_objects(grid, color):
    """
    Finds contiguous regions of a specific color in a grid.
    Uses a depth-first search algorithm.
    """
    visited = set()
    objects = []

    def dfs(row, col, current_object):
        if (row, col) in visited or not (0 <= row < len(grid) and 0 <= col < len(grid[0])) or grid[row][col] != color:
            return
        visited.add((row, col))
        current_object.append((row, col))
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)


    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == color and (row, col) not in visited:
                current_object = []
                dfs(row, col, current_object)
                objects.append(current_object)
    return objects

def transform(input_grid):
    # Find all blue (1) objects
    blue_objects = find_objects(input_grid, 1)

    # Count the number of distinct blue objects
    object_count = len(blue_objects)

    # Initialize output_grid
    output_grid = []

    # Construct the beginning of output
    for _ in range(object_count):
       output_grid.append(1)
    
    # Construct the end of output
    output_grid.append(0)

    return output_grid
```