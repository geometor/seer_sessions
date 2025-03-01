"""
1.  **Find the green pixel:** Locate the single green (3) pixel in the input grid. Note its row and column.
2.  **Draw green lines**: In the output grid, draw a vertical line and a horizontal line of green (3) pixels.
    *   The vertical line is at the same column as the original green pixel in the input.
    *   The Horizontal line is at the same row as the original green pixel in the input.
    *   All cells of lines will have value of 3, no empty values.
3.  **Add Gray Highlights**: Add gray (5) pixels in two location:
    *   replace original green pixel location with '5'
    *   replace cell at (row, column) where column = original_column - 1
"""

import numpy as np

def find_pixel_by_color(grid, color):
    """Finds the coordinates of the first pixel of a given color."""
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color:
                return (r, c)
    return None

def transform(input_grid):
    """Transforms the input grid according to the described rule."""
    output_grid = np.zeros_like(input_grid)
    rows, cols = output_grid.shape

    # 1. Find the green pixel.
    green_pixel_pos = find_pixel_by_color(input_grid, 3)

    if green_pixel_pos is None:
        return output_grid  # Return empty if no green pixel (should not happen based on description).

    green_row, green_col = green_pixel_pos

    # 2. Draw green lines.
    for r in range(rows):
        output_grid[r, green_col] = 3  # Vertical line
    for c in range(cols):
        output_grid[green_row, c] = 3  # Horizontal line

    # 3. Add Gray Highlights.
    output_grid[green_row, green_col] = 5  # Replace original green pixel
    if green_col > 0:
      output_grid[green_row, green_col -1] = 5

    return output_grid