# 48d8fb45 • 017 • refine_coder

---
```python
"""
1.  **Identify Red Objects:** Locate all contiguous regions of red (color value 2) pixels in the input grid.  A contiguous region is defined as a group of one or more red pixels that are directly adjacent (up, down, left, or right – not diagonally).
2.  **Determine Bounding Box:** Calculate the smallest rectangular bounding box that encompasses all identified red objects. The bounding box is defined by the minimum and maximum row and column indices of the red pixels.
3.  **Create Output Grid:** Create a new grid whose dimensions match the size of the bounding box.
4. **Fill The Bounding Box:** Fill the output grid with red pixels.
"""

import numpy as np

def get_objects(grid, color=None):
    """Identifies contiguous objects of the specified color in the grid."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, current_object):
        """Depth-First Search to find contiguous pixels of the same color."""
        if (
            row < 0
            or row >= grid.shape[0]
            or col < 0
            or col >= grid.shape[1]
            or visited[row, col]
            or (color is not None and grid[row, col] != color)
        ):
            return

        visited[row, col] = True
        current_object.append((row, col))

        # Explore adjacent pixels
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col] and (color is None or grid[row, col] == color):
                current_object = []
                dfs(row, col, current_object)
                if current_object:
                    objects.append(current_object)
    return objects

def get_bounding_box(objects):
    """Calculates the bounding box for a list of objects."""
    if not objects:
        return None

    min_row = min(pixel[0] for obj in objects for pixel in obj)
    max_row = max(pixel[0] for obj in objects for pixel in obj)
    min_col = min(pixel[1] for obj in objects for pixel in obj)
    max_col = max(pixel[1] for obj in objects for pixel in obj)

    return (min_row, min_col, max_row, max_col)

def transform(input_grid):
    """
    Identifies red objects and creates a minimum bounding box
    """
    #Identify Red Objects
    red_objects = get_objects(input_grid, 2)
    
    #Determine Bounding Box
    bounding_box = get_bounding_box(red_objects)
    
    #Create Output Grid:
    if bounding_box is None:
        return np.zeros((1, 1), dtype=int)
        
    min_row, min_col, max_row, max_col = bounding_box
    output_grid = np.zeros((max_row - min_row + 1, max_col - min_col + 1), dtype=int)
    
    #Fill The Bounding Box
    for obj in red_objects:
        for row, col in obj:
            output_grid[row-min_row,col-min_col] = 2

    return output_grid
```
