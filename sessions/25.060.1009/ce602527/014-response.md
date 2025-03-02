# ce602527 • 014 • refine_coder

---
```python
"""
1.  **Identify the Background:** The background color is the color of the top-left pixel of the input grid.
2.  **Find the Target Object:** Find the *smallest* object in the input that is not the background color, regardless of shape.
3. **Determine Output Grid:**
    * output width: input width + number of columns
    * output height: input height + 1
4.  **Recreate the Target Object:** Copy the target object to the output grid.
5.  **Position:** The target object's row in the output is the same as in the input. The target object's column position in the output is input columns / 2 + 1.
"""

import numpy as np

def find_objects(grid):
    """
    Identifies distinct objects in the grid.
    Returns a dictionary of objects, keyed by color.
    Each object is a list of (row, col) tuples.
    """
    objects = {}
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, obj_pixels):
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or visited[row, col]
            or grid[row, col] != color
        ):
            return
        visited[row, col] = True
        obj_pixels.append((row, col))
        dfs(row + 1, col, color, obj_pixels)
        dfs(row - 1, col, color, obj_pixels)
        dfs(row, col + 1, color, obj_pixels)
        dfs(row, col - 1, color, obj_pixels)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col]:
                color = grid[row, col]
                obj_pixels = []
                dfs(row, col, color, obj_pixels)
                if color not in objects:
                    objects[color] = []
                objects[color].append(obj_pixels)
    return objects

def find_smallest_non_background_object(grid):
    """
    Finds the smallest object that isn't the background color.
    """
    background_color = grid[0, 0]
    objects = find_objects(grid)
    smallest_object = None
    smallest_size = float('inf')

    for color, obj_list in objects.items():
        if color != background_color:
            for obj in obj_list:
                if len(obj) < smallest_size:
                    smallest_size = len(obj)
                    smallest_object = obj
    return smallest_object

def transform(input_grid):
    # Identify the background color
    background_color = input_grid[0, 0]

    # Find the target object (smallest non-background object)
    target_object = find_smallest_non_background_object(input_grid)

    # Determine output grid size
    output_height = input_grid.shape[0] + 1
    output_width = input_grid.shape[1] + 3
    output_grid = np.full((output_height, output_width), background_color, dtype=int)

    # If no target object is found, return a grid of the background color.
    if target_object is None:
        return output_grid
    
    #find target color
    target_color = input_grid[target_object[0]]

    # Recreate the target object in the output grid
    target_row = target_object[0][0]
    target_col = target_object[0][1]
    output_col = input_grid.shape[1] // 2 + 1

    output_grid[target_row , output_col] = target_color

    return output_grid
```
