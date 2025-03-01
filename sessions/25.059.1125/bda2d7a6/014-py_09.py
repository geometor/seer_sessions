"""
1.  **Identify the Outer Orange Rectangle:** Find the bounding box of the largest contiguous block of orange pixels. This defines the "outer orange rectangle."
2.  **Identify Inner Magenta Rectangle:** Find the bounding box of the contiguous block of magenta pixels inside the outer orange rectangle.
3. **Color Transformations:**
      *   All pixels *outside* the "outer orange rectangle" that are white become magenta.
      *   Within the "outer orange rectangle", all orange pixels become white.
      *   Within the "outer orange rectangle", all magenta pixels become orange.
"""

import numpy as np

def find_bounding_box(grid, color):
    """Finds the bounding box of the largest contiguous block of the specified color."""
    rows, cols = grid.shape
    min_row, min_col = rows, cols
    max_row, max_col = -1, -1

    for i in range(rows):
        for j in range(cols):
            if grid[i, j] == color:
                min_row = min(min_row, i)
                min_col = min(min_col, j)
                max_row = max(max_row, i)
                max_col = max(max_col, j)

    if max_row == -1: # no object found
       return None
    return [min_row, min_col, max_row, max_col]

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""

    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find the outer orange rectangle.
    orange_bbox = find_bounding_box(output_grid, 7)

    # Find the inner magenta rectangle.
    magenta_bbox = find_bounding_box(output_grid, 6)

    # Iterate through the grid and apply transformations.
    for i in range(rows):
        for j in range(cols):
            # Fill surrounding area.
            if orange_bbox is not None and not (orange_bbox[0] <= i <= orange_bbox[2] and
                    orange_bbox[1] <= j <= orange_bbox[3]):
                if output_grid[i, j] == 0:
                    output_grid[i, j] = 6
            # Invert colors within the orange rectangle.
            elif orange_bbox is not None:
                if output_grid[i,j] == 7:
                  output_grid[i,j] = 0
                elif output_grid[i,j] == 6:
                  output_grid[i,j] = 7

    return output_grid