"""
1. **Identify:** Find all orange pixels (value 7) in the input grid.
2. **Bound:** Determine the minimum and maximum row and column indices among the identified orange pixels. This defines the top-left and bottom-right corners of a rectangle.
3. **Fill:** In the output grid, set all pixels within the boundaries of the rectangle (inclusive) to orange (value 7). Pixels outside this rectangle remain unchanged (white/0). The input grid dimensions are maintained.
"""

import numpy as np

def find_orange_pixels(grid):
    # Find coordinates of all orange pixels (value 7).
    orange_pixels = []
    for row_index, row in enumerate(grid):
        for col_index, pixel in enumerate(row):
            if pixel == 7:
                orange_pixels.append((row_index, col_index))
    return orange_pixels

def create_bounding_rectangle(orange_pixels):
    # Determine the minimum and maximum row and column indices.
    if not orange_pixels:
        return None, None, None, None  # Handle cases with no orange pixels
    min_row, min_col = orange_pixels[0]
    max_row, max_col = orange_pixels[0]
    for row, col in orange_pixels:
        min_row = min(min_row, row)
        min_col = min(min_col, col)
        max_row = max(max_row, row)
        max_col = max(max_col, col)
    return min_row, min_col, max_row, max_col

def transform(input_grid):
    # Initialize output grid with the same dimensions and default white pixels.
    output_grid = np.zeros_like(input_grid)

    # Find all orange pixels.
    orange_pixels = find_orange_pixels(input_grid)

    # Create bounding rectangle.
    min_row, min_col, max_row, max_col = create_bounding_rectangle(orange_pixels)

    if min_row is not None: # Handle potential case of no orange pixels in input.
      # Fill the rectangle with orange.
      for row in range(min_row, max_row + 1):
          for col in range(min_col, max_col + 1):
              output_grid[row, col] = 7

    return output_grid