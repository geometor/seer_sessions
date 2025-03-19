# 9aec4887 • 014 • refine_coder

---
```python
"""
The transformation identifies each contiguous region (object) of non-zero pixels in the input grid.  For each object, it determines the minimum bounding box and extracts the color. It then constructs a 5x5 output grid, filling it with a representation of each object based on its color. The object color is placed in a specific pattern in the output, repeating the color at certain offsets.
"""

import numpy as np

def get_objects(grid):
    """
    Finds contiguous regions of non-zero colors in the grid.
    Returns a dictionary of objects, where keys are colors and values are lists of (row, col) coordinates.
    """
    objects = {}
    visited = set()

    def dfs(row, col, color):
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or (row, col) in visited
            or grid[row, col] != color
        ):
            return []

        visited.add((row, col))
        coords = [(row, col)]
        coords.extend(dfs(row + 1, col, color))
        coords.extend(dfs(row - 1, col, color))
        coords.extend(dfs(row, col + 1, color))
        coords.extend(dfs(row, col - 1, color))
        return coords

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            color = grid[row, col]
            if color != 0 and (row, col) not in visited:
                coords = dfs(row, col, color)
                if color not in objects:
                    objects[color] = []
                objects[color].extend(coords)  # Extends the objects color list with coordinates.
    return objects


def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((5, 5), dtype=int)
    
    # identify objects
    objects = get_objects(input_grid) # dictionary: color -> list of coordinates

    # positions to fill in output grid
    positions = [(1, 1), (2, 1), (3, 1), (4, 1), (1, 3), (2, 3), (3, 3), (4, 3)]
    pos_idx = 0

    # iterate through each object and place its color in the output grid
    for color in sorted(objects.keys()): # Ensure consistent order
        if pos_idx < len(positions):
           row1, col1 = positions[pos_idx]
           output_grid[row1, col1] = color
           pos_idx += 1
        if pos_idx < len(positions):
           row2, col2 = positions[pos_idx]
           output_grid[row2, col2] = color
           pos_idx += 1          
    
    return output_grid
```
