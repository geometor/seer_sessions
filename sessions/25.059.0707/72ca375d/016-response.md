# 72ca375d • 016 • example_3 • investigate_coder

---
```python
"""
Identify the gray (5) colored object cluster within the input grid. Ignore other objects and background. Enclose a rectangular region around gray object in output. Output a simplified gray object as 2 x 4 grid.
"""

import numpy as np

def get_objects(grid, background_color=0):
    """
    Finds objects in the grid, excluding the background color.
    Returns a dictionary of objects keyed by color.
    """
    objects = {}
    visited = set()

    def dfs(row, col, color, object_pixels):
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
            return
        visited.add((row, col))
        object_pixels.append((row, col))
        dfs(row + 1, col, color, object_pixels)
        dfs(row - 1, col, color, object_pixels)
        dfs(row, col + 1, color, object_pixels)
        dfs(row, col - 1, color, object_pixels)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            color = grid[row, col]
            if color != background_color and (row, col) not in visited:
                object_pixels = []
                dfs(row, col, color, object_pixels)
                if color not in objects:
                    objects[color] = []
                objects[color].append(object_pixels)
    return objects
    

def transform(input_grid):
    # Find objects in the input grid.
    objects = get_objects(input_grid)
    
    # Check if gray (5) objects exist.
    if 5 not in objects:
        return np.zeros((2, 4), dtype=int)  # Return default if no gray objects

    gray_objects = objects[5]
    
    # Find bounding box of all gray objects, considering multiple gray object groups
    min_row, min_col = input_grid.shape
    max_row, max_col = -1, -1
    
    for gray_object in gray_objects:  # iterate through different gray colored objects
        for row, col in gray_object:
            min_row = min(min_row, row)
            min_col = min(min_col, col)
            max_row = max(max_row, row)
            max_col = max(max_col, col)
            
    # Handle edge cases where gray area doesn't fill 2x4
    height = max_row - min_row + 1
    width = max_col - min_col + 1

    # initialize the output grid, fill with 0s
    output_grid = np.zeros((2, 4), dtype=int)

    if height > 0 and width > 0:  # if found grey region
       # fill the output array with 5s
       output_grid[:min(2,height), :min(4,width)] = 5
    
    return output_grid
```
