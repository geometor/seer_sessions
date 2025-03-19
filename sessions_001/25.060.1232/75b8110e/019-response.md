# 75b8110e • 019 • refine_coder

---
```python
"""
1.  **Object Identification:** Identify all contiguous regions of the same color as distinct objects. Record their color and position (e.g., top-left, center, bottom-right). Note any 2x2 squares.

2. **Column Creation**:
   - create four columns as the output
3.  **Object Selection**:
    - The output always seems to have four columns, composed of the colors of
      objects found in the four corners of the input grid. The exception is when
      the bottom left is zero, then use the bottom right.
   - If one object of color 6 (magenta) is in any corner of the input, it is always the left-most column.
4. **Object Transformation:**
   - Convert each selected corner object into a single column with height of 4.
5. **Output Construction:** Arrange the transformed columns to fill the output grid in this order:
    - The left most column is the 6(magenta) if present in the input, otherwise it is from the top-left
    - The second column is the object in the top left, unless magenta was present
    - The third column is the object in the center if it is a 2x2, otherwise it
      is the color present at the input top right
    - The last column corresponds to the color in the bottom right corner.
"""

import numpy as np

def get_objects(grid):
    """
    Identifies contiguous objects and their corner positions.
    """
    objects = {}
    visited = set()
    rows, cols = grid.shape

    def dfs(r, c, color, obj):
        if (r, c) in visited or r < 0 or r >= rows or c < 0 or c >= cols or grid[r, c] != color:
            return
        visited.add((r, c))
        obj.append((r, c))
        dfs(r + 1, c, color, obj)
        dfs(r - 1, c, color, obj)
        dfs(r, c + 1, color, obj)
        dfs(r, c - 1, color, obj)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited:
                color = grid[r, c]
                obj = []
                dfs(r, c, color, obj)
                if color not in objects:
                    objects[color] = []
                objects[color].append(obj)
    return objects

def get_corner_colors(grid, objects):
    """
    Gets the colors at the corners of the grid, handling edge cases.
    """
    rows, cols = grid.shape
    top_left = grid[0, 0]
    top_right = grid[0, cols - 1]
    bottom_left = grid[rows - 1, 0]
    bottom_right = grid[rows - 1, cols - 1]
    
    # Handle cases if corner pixel is part of bigger object
    if bottom_left == 0:
        bottom_left = bottom_right

    return top_left, top_right, bottom_left, bottom_right


def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros((4, 4), dtype=int)
    rows, cols = input_grid.shape

    # get objects
    objects = get_objects(input_grid)

    # get corner colors
    top_left, top_right, bottom_left, bottom_right = get_corner_colors(input_grid, objects)
   
    # determine column order, prioritizing magenta (6)
    column_colors = [top_left, top_right, bottom_right]
    magenta_present = False

    for color in objects:
      if color == 6:
        for obj in objects[color]:
          if (0,0) in obj or (0, cols-1) in obj or (rows-1, 0) in obj or (rows-1, cols-1) in obj:
              column_colors.insert(0, 6)
              magenta_present = True
              break
        if magenta_present:
          break

    if not magenta_present:
      column_colors.insert(0, top_left)

    
    # check center for 2x2 and use that for column 3
    center_color = -1
    for color in objects:
      for obj in objects[color]:
          # Check if the object is a 2x2 square in the center
          is_2x2 = len(obj) == 4
          if is_2x2:
            row_indices, col_indices = zip(*obj)
            if (max(row_indices) - min(row_indices) == 1) and (max(col_indices)-min(col_indices) == 1):
              center_color = color
              break

    if center_color != -1:
        column_colors[2] = center_color #replace with center
    # assign columns in output
    for i, color in enumerate(column_colors):
        output_grid[:, i] = color

    return output_grid
```
