"""
1.  **Isolate Azure Pixels:** Identify all pixels with the color azure (8) in the input grid.
2.  **Discard Other Colors:** Remove all pixels that are not azure, setting their value to white (0).
3.  **Form Horizontal Line:** Create a horizontal line of azure pixels across the 11th row of the output grid.
4. **Form Vertical Line**: Create a vertical line of azure pixels from top to bottom in the middle of the grid(column 13).
5.  **Combine:** Combine horizontal line and vertical line.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid by keeping only azure pixels and arranging them in a cross shape."""

    # Initialize output grid with all white pixels (0)
    output_grid = np.zeros_like(input_grid)
    rows, cols = output_grid.shape

    # Calculate the center row and column
    center_row = 10
    center_col = 13


    # Form the horizontal line
    output_grid[center_row, :] = 8

    # Form the vertical line
    output_grid[:,center_col] = 8


    return output_grid