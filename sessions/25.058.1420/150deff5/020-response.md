# 150deff5 • 020 • refine_coder

---
```python
"""
1.  **Identify Gray Shapes:** Locate all contiguous shapes formed by gray (5) pixels in the input grid.

2.  **Process Each Shape:** For each identified gray shape:
    a.  **Find Extremes:** Determine the leftmost and rightmost x-coordinates.
    b. **Leftmost Edge:** change the color the leftmost pixels to red (2).
    c. **Rightmost Edge:** Change the color of the rightmost pixels to azure (8).
    d. **Interior Pixels, first section**: If a gray pixel has the same x value of another pixel directly above or below, and is not on the rightmost edge, change color to red (2).
    e. **Interior Pixels, second section**: All remaining pixels are colored azure (8).

3.  **Maintain Background:** All other pixels (non-5) in the grid remain unchanged.
"""

import numpy as np

def find_shapes(grid, color):
    """
    Finds contiguous shapes of the specified color and returns as list where
    one item contains coordinates for one shape
    """
    coords = np.argwhere(grid == color)
    if len(coords) == 0:
        return []

    shapes = []
    visited = set()

    def dfs(row, col, current_shape):
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
            return
        visited.add((row, col))
        current_shape.append((row, col))
        dfs(row + 1, col, current_shape)
        dfs(row - 1, col, current_shape)
        dfs(row, col + 1, current_shape)
        dfs(row, col - 1, current_shape)

    for r, c in coords:
        if (r, c) not in visited:
            current_shape = []
            dfs(r, c, current_shape)
            shapes.append(current_shape)

    return shapes

def transform(input_grid):
    # Initialize output grid with the same dimensions and background color.
    output_grid = np.copy(input_grid)

    # Find all shapes formed by '5' (gray).
    shapes = find_shapes(input_grid, 5)

    # Iterate through each shape
    for shape_coords in shapes:
      #find the leftmost and rightmost x coordinates
      x_coords = [c for r, c in shape_coords]
      min_x = np.min(x_coords)
      max_x = np.max(x_coords)

      # Replace '5's with '2's (red) or '8' (azure)
      for r, c in shape_coords:
          if c == min_x:
            output_grid[r,c] = 2  # Leftmost edge
          elif c == max_x:
            output_grid[r, c] = 8  # Rightmost edge
          else:
            # Check for neighbors above or below within the shape
            is_connected_vertically = False
            for r2, c2 in shape_coords:
              if c2 == c and (r2 == r - 1 or r2 == r + 1):
                is_connected_vertically = True
                break
            if is_connected_vertically:
              output_grid[r,c] = 2
            else:
              output_grid[r,c] = 8
    return output_grid
```
