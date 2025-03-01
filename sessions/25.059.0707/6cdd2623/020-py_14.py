"""
1.  **Initialize Output:** Create an output grid with the same dimensions as the input grid. Fill the output grid with white (0) pixels.
2.  **Calculate Center:** Determine the center row and center column of the output grid.  If the height is even, use `height // 2 - 1`.  If height is odd use `height // 2`. Do the same for columns/width.
3.  **Draw Horizontal Line:** Draw a horizontal line of azure (8) pixels across the center row of the output grid.
4.  **Draw Vertical Line:** Draw a vertical line of azure (8) pixels down the center column of the output grid.
5.  **Final Output:** Return the modified output grid.
"""

import numpy as np

def transform(input_grid):
    # Initialize output grid with all white pixels (0) and same dimensions as input
    output_grid = np.zeros_like(input_grid)
    output_grid = output_grid.astype(int)

    rows, cols = output_grid.shape

    # Calculate center row and column
    center_row = rows // 2 - 1 if rows % 2 == 0 else rows // 2
    center_col = cols // 2 - 1 if cols % 2 == 0 else cols // 2


    # Draw horizontal line at center_row
    for c in range(cols):
        output_grid[center_row, c] = 8

    # Draw vertical line at center_col
    for r in range(rows):
        output_grid[r, center_col] = 8


    return output_grid