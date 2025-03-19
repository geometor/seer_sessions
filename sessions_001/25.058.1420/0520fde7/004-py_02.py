"""
1.  **Identify Key Features:** Locate the single vertical line of gray (5) pixels and the horizontal lines of blue (1) pixels in the input grid.
2.  **Determine Intersection:** Find the pixel where a blue horizontal line and the gray vertical line intersect. Note color (1) and color (5).
3. **Create Output Grid:** Create a 3x3 output grid filled with white (0) pixels.
4. **Mark the position:** Find the center point (1,1) of a 3x3 grid.
5.  **Place Result:** At the center of the output grid (coordinates 1, 1, using 0-based indexing), change the pixel to the next color after input blue(1), red (2).
6. **Other cells:** Fill the rest of the cells with (0).
"""

import numpy as np

def find_vertical_gray_line(grid):
    """Finds the column index of the vertical gray line."""
    for j in range(grid.shape[1]):
        if all(grid[:, j] == 5):
            return j
    return -1

def find_blue_rows(grid):
    """Finds the row indices of horizontal lines containing blue pixels."""
    blue_rows = []
    for i in range(grid.shape[0]):
        if 1 in grid[i, :]:
            blue_rows.append(i)
    return blue_rows

def transform(input_grid):
    # initialize output_grid as 3x3 filled with white (0)
    output_grid = np.zeros((3, 3), dtype=int)

    # Find the column index of the vertical gray line
    gray_column_index = find_vertical_gray_line(input_grid)

    # Find the row indices of the horizontal blue lines
    blue_row_indices = find_blue_rows(input_grid)
    
    # Determine intersection and place red (2) pixel at center of output grid
    if gray_column_index != -1 and blue_row_indices:
        output_grid[1, 1] = 2 

    return output_grid