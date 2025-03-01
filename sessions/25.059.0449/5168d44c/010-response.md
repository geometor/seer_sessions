# 5168d44c • 010 • example_2 • investigate_coder

---
```python
"""
1.  **Identify Objects:** Locate the vertical green line and the red square (with a green center) within the input grid.
2.  **Green Line:** The position of the green line remains constant.
3.  **Red Square Movement:** Move the entire red square upwards by two rows. The green pixel within maintains it's relative position.
4.  **Overlap:** If the moved red square overlaps with any part of green pixels of the line, the green pixels are overwritten by the color of the red square.
5. **Output:** draw the new grid
"""

import numpy as np

def find_object(grid, color, shape_type=None):
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def is_valid(r, c):
        return 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]

    def dfs(r, c, current_object):
        if not is_valid(r, c) or visited[r, c] or grid[r, c] != color:
            return
        visited[r, c] = True
        current_object.append((r, c))
        dfs(r + 1, c, current_object)
        dfs(r - 1, c, current_object)
        dfs(r, c + 1, current_object)
        dfs(r, c - 1, current_object)


    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color and not visited[r, c]:
                current_object = []
                dfs(r, c, current_object)
                if shape_type == "line":
                  rows, cols = zip(*current_object)
                  if all(x == cols[0] for x in cols):
                    objects.append(current_object)

                elif shape_type == "rectangle":
                    rows, cols = zip(*current_object)
                    min_row, max_row = min(rows), max(rows)
                    min_col, max_col = min(cols), max(cols)
                    if len(current_object) == (max_row - min_row + 1) * (max_col-min_col + 1):
                      objects.append(current_object)

                else:
                  objects.append(current_object)

    return objects

def move_object(grid, object_coords, dr, dc):
    new_object_coords = []
    for r, c in object_coords:
        new_object_coords.append((r + dr, c + dc))
    return new_object_coords

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Find the green line.
    green_lines = find_object(input_grid, 3, "line")
    green_line = None

    #find a vertical line
    for line in green_lines:
        rows, cols = zip(*line)
        if len(set(cols)) == 1:
            green_line = line
            break


    # Find the red square.
    red_squares = find_object(input_grid, 2, "rectangle")
    red_square = None
    for square in red_squares:
        #check if it is really a square/rectangle
        rows, cols = zip(*square)
        min_row, max_row = min(rows), max(rows)
        min_col, max_col = min(cols), max(cols)

        if (max_row - min_row + 1) * (max_col - min_col + 1) == len(square):
            red_square = square
            break


    # Move the red square up by two rows.
    if red_square:
       new_red_square = move_object(input_grid, red_square, -2, 0)

       #clear previous position from output
       for r,c in red_square:
          output_grid[r,c] = 0


       #apply to the new position
       for r, c in new_red_square:
        if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:

            output_grid[r, c] = 2 #set as red

    # Find center of the red object in the input
    if red_square:

      rows, cols = zip(*red_square)
      min_row, max_row = min(rows), max(rows)
      min_col, max_col = min(cols), max(cols)
      center_row = (min_row+max_row)//2
      center_col = (min_col+max_col)//2

      #copy the center pixel after moving two rows up
      if input_grid[center_row, center_col] == 3:
        new_center_row = center_row - 2
        if 0 <= new_center_row < output_grid.shape[0] and 0 <= center_col < output_grid.shape[1]:
          output_grid[new_center_row,center_col] = 3

    return output_grid
```
