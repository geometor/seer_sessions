# 5c0a986e • 014 • refine_coder

---
```python
"""
1.  **Identify Objects:** Find all contiguous regions (objects) of red (2) and blue (1) pixels in the input grid.
2. **Conditional Transformation:**
   - If there's exactly one red object and one blue object:
     - Check relative postion of Red and Blue objects.
       - Sometimes a line is drawn between the objects using pixels of color blue (1).
       - Sometimes no changes are made.
   - Otherwise: No transformation.
3. **Preservation:** The original red and blue objects always remain.
"""

import numpy as np

def find_objects(grid, color):
    """Finds contiguous regions of a specific color."""
    objects = []
    visited = set()

    def dfs(row, col):
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
            return []

        visited.add((row, col))
        region = [(row, col)]

        region.extend(dfs(row + 1, col))
        region.extend(dfs(row - 1, col))
        region.extend(dfs(row, col + 1))
        region.extend(dfs(row, col - 1))
        return region

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color and (r, c) not in visited:
                objects.append(dfs(r, c))
    return objects

def find_extrema(object_pixels):
    """Finds the top-left and bottom-right pixels of an object."""
    if not object_pixels:
        return None, None

    min_row = min(pixel[0] for pixel in object_pixels)
    max_row = max(pixel[0] for pixel in object_pixels)
    min_col = min(pixel[1] for pixel in object_pixels)
    max_col = max(pixel[1] for pixel in object_pixels)

    top_left = (min_row, min_col)
    bottom_right = (max_row, max_col)

    for r, c in object_pixels:
      if r == min_row and c < top_left[1]:
        top_left = (r,c)
      if r == max_row and c > bottom_right[1]:
        bottom_right = (r, c)

    return top_left, bottom_right

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    grid = np.array(input_grid)

    # Find red and blue objects
    red_objects = find_objects(grid, 2)
    blue_objects = find_objects(grid, 1)

    # Conditional Transformation based on number of red/blue objects
    if len(red_objects) == 1 and len(blue_objects) == 1:
        red_object = red_objects[0]
        blue_object = blue_objects[0]
        
        # find extrema
        _, red_bottom_right = find_extrema(red_object)
        blue_top_left, _ = find_extrema(blue_object)
        red_top_left, _ = find_extrema(red_object)

        r_row, r_col = red_bottom_right
        b_row, b_col = blue_top_left
        
        # Example 1: Connect with a diagonal
        if r_row < b_row and r_col < b_col:
            # draw diagonal line
            current_row = r_row + 1
            current_col = r_col + 1

            row_step = 1
            col_step = 1
            while current_row <= b_row and current_col <= b_col:
               if 0 <= current_row < output_grid.shape[0] and 0 <= current_col < output_grid.shape[1]:
                  output_grid[current_row, current_col] = 1
               current_row += row_step
               current_col += col_step
        # Example 3: Add one blue
        elif r_row > b_row and r_col < b_col:
           output_grid[red_top_left[0]-1, red_top_left[1]] = 1
        # examples 2 and 4 - do nothing

    return output_grid
```
