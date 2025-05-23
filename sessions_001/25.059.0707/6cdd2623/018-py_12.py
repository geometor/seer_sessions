"""
1.  **Initialize Output:** Create an output grid of the same dimensions as the input grid, filled with white (0).
2.  **Draw Horizontal Line:** Draw a horizontal line of azure (8) pixels across the 11th row (index 10) of the output grid.
3.  **Draw Vertical Line:** Draw a vertical line of azure (8) pixels down the 14th column (index 13) of the output grid.
4.  **Final Output:** Return the modified output grid.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid by creating a cross shape of azure pixels."""

    # Initialize output grid with all white pixels (0) and same dimensions as input
    output_grid = np.zeros_like(input_grid)
    output_grid = output_grid.astype(int)

    rows, cols = output_grid.shape

    # Draw horizontal line at row 10
    for c in range(cols):
        output_grid[10, c] = 8

    # Draw vertical line at column 13
    for r in range(rows):
        output_grid[r, 13] = 8


    return output_grid