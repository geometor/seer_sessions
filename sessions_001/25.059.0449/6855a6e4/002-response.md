# 6855a6e4 • 002 • example_3 • investigate_coder

---
```python
"""
1.  **Identify Objects:** Find all contiguous red (2) pixels, forming the "red shape," and all gray (5) pixels, forming the initial "gray shapes."

2.  **Determine Gray Shape Target Area:** Identify the horizontal center of the "red shape".

3.  **Reposition and Merge Gray:** Move each disconnected originally gray area.
    *   Gray pixels stay in original columns.
    *   Gray pixels move to rows closest to identified horizontal center.
    *    Merge gray pixels inside the "red shape" if some gray pixels are contained.
    *   Gray pixels move outside and in contact with the red shape if no gray pixels inside red shape.

4.  **Output:** The final grid contains the original red shape and the repositioned, merged gray shape.
"""

import numpy as np

def find_objects(grid, color):
    """Finds contiguous objects of a given color in the grid."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, current_object):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        current_object.append((row, col))
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if grid[row, col] == color and not visited[row, col]:
                current_object = []
                dfs(row, col, current_object)
                objects.append(current_object)
    return objects

def get_bounding_box(obj):
    """
    returns topleft and bottom right corner coordinates
    """
    rows = [r for r, _ in obj]
    cols = [c for _, c in obj]
    return min(rows), min(cols), max(rows), max(cols)

def calculate_center(obj):
    """Calculates the geometric center of an object."""
    rows = [r for r, _ in obj]
    cols = [c for _, c in obj]
    return (sum(rows) / len(rows), sum(cols) / len(cols))

def transform(input_grid):
    """Transforms the input grid according to the observed rules."""
    grid = np.array(input_grid)
    output_grid = np.copy(grid)

    # 1. Identify Objects
    red_objects = find_objects(grid, 2)
    gray_objects = find_objects(grid, 5)
    
    if not red_objects or not gray_objects:
        return output_grid.tolist()  # Return original if no red or gray objects

    # Assuming only one red object for now
    red_object = red_objects[0]

    # 2. Determine Gray Shape Target Area
    red_center_row, _ = calculate_center(red_object)
    
    # Calculate initial gray bounding box to help later
    gray_pixels = [pixel for obj in gray_objects for pixel in obj]
    gray_top, gray_left, gray_bottom, gray_right = get_bounding_box(gray_pixels)

    # Clear original gray pixels, keep track of original position
    gray_positions = []
    for obj in gray_objects:
      for r,c in obj:
        output_grid[r][c] = 0
        gray_positions.append((r,c))
    
    # Sort gray pixels by column for relative repositioning
    gray_positions.sort(key=lambda x: x[1])
    
    gray_rows = [r for r,_ in gray_positions]
    gray_cols = [c for _,c in gray_positions]
    
    # determine how to arrange gray pixels
    new_gray_rows = []
    top_target = int(round(red_center_row - (gray_bottom - gray_top) / 2))
    for i in range(len(gray_cols)):
        new_gray_rows.append(top_target + (gray_rows[i] - gray_top)) # apply the shift
    
    # Reposition gray
    for i in range(len(gray_cols)):
      output_grid[new_gray_rows[i], gray_cols[i]] = 5
    
    return output_grid.tolist()
```
