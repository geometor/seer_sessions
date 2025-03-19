# 2bee17df • 007 • refine_coder

---
```python
"""
1.  **Identify the Azure Frame:** Find the outermost rectangle of azure (8) pixels.
2.  **Identify the Inner White region:** Within the azure frame, locate the contiguous rectangular region of white (0) pixels.
3.  **Locate the Red Pixel:** Find the single red (2) pixel within the azure frame.
4.  **Fill with Green:** Change all white (0) pixels within the inner white region to green (3), *except* for any white pixel that shares an edge (up, down, left, or right) with the red pixel.
"""

import numpy as np

def get_neighbors(grid, row, col):
    """Returns a list of neighbors (up, down, left, right) for a given cell."""
    neighbors = []
    rows, cols = grid.shape
    if row > 0:
        neighbors.append((row - 1, col))  # Up
    if row < rows - 1:
        neighbors.append((row + 1, col))  # Down
    if col > 0:
        neighbors.append((row, col - 1))  # Left
    if col < cols - 1:
        neighbors.append((row, col + 1))  # Right
    return neighbors

def find_azure_frame(grid):
    """Finds the outermost rectangle of azure pixels."""
    rows, cols = grid.shape
    top, bottom, left, right = 0, rows - 1, 0, cols - 1

    # Find top and bottom boundaries
    while top < rows and np.all(grid[top, :] == 8):
        top += 1
    while bottom >= 0 and np.all(grid[bottom, :] == 8):
        bottom -= 1

    # Find left and right boundaries
    while left < cols and np.all(grid[:, left] == 8):
        left += 1
    while right >= 0 and np.all(grid[:, right] == 8):
        right -= 1

    return top, bottom, left, right


def find_white_region(grid, top, bottom, left, right):
    """Finds the inner white region within the azure frame."""
    # Initialize to frame boundaries + 1, assuming at least one layer of azure
    inner_top, inner_bottom = top, bottom
    inner_left, inner_right = left, right

    if top < bottom and left < right:
      # find first non-azure
      for r in range(top, bottom + 1):
          if grid[r, left] != 8:
              inner_top = r
              break

      for r in range(bottom, top -1, -1):
          if grid[r, left] != 8:
              inner_bottom = r
              break

      for c in range(left, right +1):
        if grid[top, c] != 8:
          inner_left = c
          break
      
      for c in range(right, left -1, -1):
        if grid[top, c] != 8:
          inner_right = c
          break

    return inner_top, inner_bottom, inner_left, inner_right

def find_red_pixel(grid):
    """Locates the red pixel within the grid."""
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 2:
                return (r, c)
    return None

def transform(input_grid):
    """Transforms the input grid according to the observed rules."""
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # 1. Identify the Azure Frame
    top, bottom, left, right = find_azure_frame(output_grid)

    # 2. Identify the Inner White region
    inner_top, inner_bottom, inner_left, inner_right = find_white_region(output_grid, top, bottom, left, right)


    # 3. Locate the Red Pixel
    red_pixel_coords = find_red_pixel(output_grid)

    # 4. Fill with Green (with exception for red pixel adjacency)
    for r in range(inner_top, inner_bottom + 1):
        for c in range(inner_left, inner_right + 1):
            if output_grid[r, c] == 0:
                if red_pixel_coords:
                    is_adjacent_to_red = False
                    for nr, nc in get_neighbors(output_grid, r, c):
                        if (nr, nc) == red_pixel_coords:
                            is_adjacent_to_red = True
                            break
                    if not is_adjacent_to_red:
                        output_grid[r, c] = 3
                else:
                    output_grid[r, c] = 3  # Fill with green if no red pixel

    return output_grid
```
