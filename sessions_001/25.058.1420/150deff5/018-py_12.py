"""
1.  **Identify Gray Shapes:** Locate all contiguous shapes formed by the digit '5' (gray) in the input grid.  There may be multiple, distinct shapes.
2.  **Process Each Shape:** For *each* identified gray shape:
    a. **Find Extremes:** Determine the leftmost and rightmost x-coordinates (horizontal positions) of the shape.
    b. **Split and Replace:** Replace the gray pixels within that shape.
        *   Pixels at the leftmost x-coordinate become '2' (red).
        *   Pixels at the rightmost x-coordinate become '8' (azure).
        *  Other pixels: those closer to leftmost are colored red (2), and those closer to rightmost, azure (8).
3.  **Maintain Background:** All other cells in the grid (those not part of any identified gray shape) remain unchanged.
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

      # Replace '5's with '2's (red) or '8' (azure) based on the vertical split
      for r, c in shape_coords:
          if c == min_x:
            output_grid[r,c] = 2
          elif c == max_x:
            output_grid[r, c] = 8
          elif abs(c - min_x) < abs(c-max_x):
            output_grid[r, c] = 2
          else:
            output_grid[r, c] = 8

    return output_grid