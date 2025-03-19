# 6b9890af • 018 • refine_coder

---
```python
"""
1.  Identify the blue object: Find the contiguous blue (color 1) object in the input grid.
2.  Determine output grid size: The output grid is a square.  Its side length is equal to the side length of the blue square plus two. Create a grid of this size and fill it with red (color 2).
3.  Copy Blue Object:** Copy the blue square from the input grid to the center of the output grid. The center of the blue object should be at output grid row = side / 2, col = side /2 (integer division)
4. Copy surrounding frame:** Copy the surrounding pixels of the blue object with a frame of 1, centered on the blue object.
"""

import numpy as np

def find_objects(grid):
    # Find distinct objects (contiguous regions of the same color)
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, color, obj_pixels):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        obj_pixels.append((row, col))
        dfs(row + 1, col, color, obj_pixels)
        dfs(row - 1, col, color, obj_pixels)
        dfs(row, col + 1, color, obj_pixels)
        dfs(row, col - 1, color, obj_pixels)

    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if not visited[i, j] and grid[i,j]!=0:
                obj_pixels = []
                dfs(i, j, grid[i, j], obj_pixels)
                if obj_pixels:
                    objects.append(obj_pixels)
    return objects

def get_object_bounds(obj_pixels):
    # Get the bounding box of an object
    min_row = min(p[0] for p in obj_pixels)
    max_row = max(p[0] for p in obj_pixels)
    min_col = min(p[1] for p in obj_pixels)
    max_col = max(p[1] for p in obj_pixels)
    return min_row, max_row, min_col, max_col

def get_object_dimensions(obj_pixels):
    # Get the dimensions (height, width) of an object
    min_row, max_row, min_col, max_col = get_object_bounds(obj_pixels)
    return max_row - min_row + 1, max_col - min_col + 1

def transform(input_grid):
    # Find objects in the input grid
    objects = find_objects(input_grid)

    # Identify the blue object
    blue_square = None
    for obj in objects:
        color = input_grid[obj[0][0], obj[0][1]]
        if color == 1:
            blue_square = obj
            break  # Assuming there's only one blue object

    # Determine output grid size
    blue_height, blue_width = get_object_dimensions(blue_square)
    output_side = max(blue_height, blue_width) + 2
    output_grid = np.full((output_side, output_side), 2, dtype=int)

    # Calculate center offsets
    center_row_out = output_side // 2
    center_col_out = output_side // 2

    min_row_b, max_row_b, min_col_b, max_col_b = get_object_bounds(blue_square)
    center_row_blue = (min_row_b + max_row_b) // 2
    center_col_blue = (min_col_b + max_col_b) // 2

    row_offset = center_row_out - center_row_blue
    col_offset = center_col_out - center_col_blue
    
    # Copy the surrounding frame and the blue object
    for row in range(min_row_b - 1, max_row_b + 2):
      for col in range(min_col_b - 1, max_col_b + 2):
        new_row = row + row_offset
        new_col = col + col_offset
        if 0 <= row < input_grid.shape[0] and 0 <= col < input_grid.shape[1]:
            if 0 <= new_row < output_side and 0 <= new_col < output_side:
                output_grid[new_row,new_col] = input_grid[row,col]

    return output_grid
```
