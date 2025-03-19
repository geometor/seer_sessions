# 150deff5 • 013 • refine_coder

---
```python
"""
1.  **Identify the Gray Shape:** Find all pixels with the color gray (value 5). These pixels form a single, contiguous shape.
2.  **Identify Exterior Boundary:** Determine the exterior boundary (edge) pixels of the gray shape. An edge pixel is defined as a gray pixel that has at least one adjacent (up, down, left, or right - not diagonal) pixel that is *not* gray.
3.  **Recolor the Edge:** Change the color of all identified edge pixels to azure (value 8).
4.  **Recolor the Interior:** Change the color of all remaining gray pixels (those not on the edge) to red (value 2).
5. **Leave Other Pixels Unchanged:** Do not alter pixels of other colors.
"""

import numpy as np

def _is_edge_pixel(grid, row, col, shape_color):
    """Checks if a pixel at (row, col) is an edge pixel of the given shape color."""
    rows, cols = grid.shape
    # Check adjacent pixels (up, down, left, right)
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < rows and 0 <= new_col < cols:
            if grid[new_row, new_col] != shape_color:
                return True  # Found a non-shape-color neighbor
        else:
            return True # edge of grid is an edge
    return False  # All neighbors are of the same shape color


def _find_shape(grid, color):
    """Finds all pixels of the specified color and returns them as a list of (row, col) tuples."""
    pixels = np.argwhere(grid == color)
    if len(pixels) == 0:
        return []
    return [(r, c) for r, c in pixels]

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""

    # Initialize output grid
    output_grid = np.copy(input_grid)
    gray_pixels = _find_shape(input_grid, 5)
    if not gray_pixels:
      return output_grid

    # Identify and recolor edge pixels
    edge_pixels = []
    for r, c in gray_pixels:
        if _is_edge_pixel(input_grid, r, c, 5):
            edge_pixels.append((r,c))
            output_grid[r, c] = 8  # Azure

    # Recolor interior pixels
    for r, c in gray_pixels:
      if (r,c) not in edge_pixels:
        output_grid[r, c] = 2    # Red
    return output_grid
```
