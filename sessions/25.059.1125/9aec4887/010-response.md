# 9aec4887 • 010 • example_2 • investigate_coder

---
```python
"""
The transformation extracts specific color, and shape information from the input grid, compresses, and rearranges it into a condensed output grid.
1. Identify Objects: Locate all distinct contiguous colored regions (objects) in the input grid.
2.  Bounding Box: find minimum bounding box that encloses all non-zero pixels.
3. Extract Corners: For each object, create a representation that has 4 pixels, each from the corner of the original object.
4.  Order Colors: Order the colored corner representation using column-major ordering (reading down each column top to bottom, left to right.)
5. Combine: Combine the 4-pixel representations to create the output
6. Resize: size of the output should always be 5x5, so fill remainder of unused area with 0.

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
                objects[color].extend(coords) # Extends the objects color list with coordinates.
    return objects

def get_bounding_box(grid):
    """
    Finds the minimum bounding box enclosing all non-zero pixels.

    """
    rows, cols = np.where(grid != 0)
    if len(rows) == 0:  # Handle empty grid case
        return (0,0,0,0)
    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)

    return min_row, max_row, min_col, max_col


def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((5, 5), dtype=int)
    objects = get_objects(input_grid) # dictionary: color -> list of coordinates
    min_row, max_row, min_col, max_col = get_bounding_box(input_grid)
    
    corners = []
    
    # Extract the color values at each of the bounding box corners.
    corners.append(input_grid[min_row, min_col]) # Top Left
    corners.append(input_grid[min_row, max_col]) # Top Right
    corners.append(input_grid[max_row, min_col]) # Bottom Left
    corners.append(input_grid[max_row, max_col]) # Bottom Right
    
    
    # Build output using colum-major ordering of corner colors
    output_grid[0, 1] = corners[0] if corners[0] != 0 else 0
    output_grid[1, 0] = corners[2] if corners[2] != 0 else 0
    output_grid[2, 0] = corners[2] if corners[2] != 0 else 0
    output_grid[3, 0] = corners[2] if corners[2] != 0 else 0
    output_grid[4, 1] = corners[0] if corners[0] != 0 else 0
    
    output_grid[0, 2] = corners[0] if corners[0] != 0 else 0
    output_grid[1, 2] = corners[3] if corners[3] != 0 else 0    
    output_grid[2, 2] = corners[3] if corners[3] != 0 else 0
    output_grid[3, 2] = corners[0] if corners[0] != 0 else 0
    output_grid[4, 2] = corners[0] if corners[0] != 0 else 0    
    
    output_grid[0, 3] = corners[1] if corners[1] != 0 else 0
    output_grid[1, 3] = corners[1] if corners[1] != 0 else 0
    output_grid[2, 3] = corners[3] if corners[3] != 0 else 0    
    output_grid[3, 3] = corners[3] if corners[3] != 0 else 0    
    output_grid[4, 3] = corners[1] if corners[1] != 0 else 0
    
    output_grid[0, 4] = corners[1] if corners[1] != 0 else 0
    output_grid[1, 4] = corners[1] if corners[1] != 0 else 0    
    output_grid[2, 4] = corners[1] if corners[1] != 0 else 0
    output_grid[3, 4] = corners[1] if corners[1] != 0 else 0


    return output_grid
```
