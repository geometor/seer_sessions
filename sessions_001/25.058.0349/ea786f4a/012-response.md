# ea786f4a • 012 • refine_coder

---
```python
"""
1. Find the Center: Determine the center pixel of the input grid.
2. Preserve the Center: The color of the center pixel in the output grid remains the same as in the input grid.
3. Checkerboard Propagation: Starting from the center pixel, propagate outwards in a checkerboard pattern, but only fill pixels that were originally white (0).
4. Color Rule:
    *   If a pixel was originally white (0), and it's being considered for filling:
        *   If the neighboring pixel (orthogonal or diagonal) being considered from has the same color as the center, fill with the alternating color.
        *   If the neighboring pixel has a different color than the center, fill with the center color
    *   If the center pixel is white (0), the alternating color used is red (2).
    *   If the center pixel is red (2), the alternating color is white (0).
"""

import numpy as np

def get_center(grid):
    """Finds the center coordinates of a grid."""
    rows, cols = grid.shape
    center_row = rows // 2
    center_col = cols // 2
    return center_row, center_col

def transform(input_grid):
    """Transforms the input grid based on a checkerboard expansion from the center."""
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    center_row, center_col = get_center(input_grid)

    # Preserve the center pixel
    center_color = input_grid[center_row, center_col]
    output_grid[center_row, center_col] = center_color

    # Determine the alternating color
    if center_color == 0:
        alt_color = 2
    elif center_color == 2:
        alt_color = 0
    else:
        alt_color = None  # Should not happen, based on problem definition

    # Create a set to store the coordinates of pixels to be processed
    processed = set()
    to_process = [(center_row, center_col)]

    while to_process:
      r, c = to_process.pop(0)
      processed.add( (r,c) )

      current_color = output_grid[r, c]
      adjacent_coords = []

      #orthogonal
      if r > 0:
        adjacent_coords.append((r - 1, c))  # Up
      if r < rows - 1:
          adjacent_coords.append((r + 1, c))  # Down
      if c > 0:
          adjacent_coords.append((r, c - 1))  # Left
      if c < cols - 1:
          adjacent_coords.append((r, c + 1))  # Right
      #diagonal
      if r > 0 and c > 0:
          adjacent_coords.append((r-1, c-1))
      if r > 0 and c < cols - 1:
          adjacent_coords.append((r-1, c+1))
      if r < rows - 1 and c > 0:
          adjacent_coords.append((r+1, c-1))
      if r < rows - 1 and c < cols - 1:
        adjacent_coords.append((r+1, c+1))

      for adj_r, adj_c in adjacent_coords:
        if (adj_r, adj_c) not in processed and input_grid[adj_r, adj_c] == 0: # Only fill if the original color was 0
          if output_grid[r,c] == center_color:
            output_grid[adj_r, adj_c] = alt_color
          else:
            output_grid[adj_r, adj_c] = center_color
          to_process.append( (adj_r, adj_c) )

    return output_grid
```
