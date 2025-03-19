"""
1.  **Get Dimensions:** Determine the number of rows and columns in the *input_grid*.
2.  **Duplicate Pixels:** Create a new grid that is twice the size of the input grid in both dimensions (2*rows x 2*columns).  For each pixel in the *input_grid*, replicate its value into a 2x2 block in the new, larger grid. For example, if a pixel in the input grid has value '3' at position (0,0), then in new, larger grid assign value '3' at locations (0,0), (0,1), (1,0), (1,1).
3.  **Add Padding:** Create the final *output_grid* by adding a one-pixel border of '0' (white) around the duplicated grid. This means the *output_grid* dimensions will be (2*rows + 2) x (2*columns + 2). Fill locations on row 0 and row (2*rows+1) with zero. Fill locations on column 0 and (2*cols + 1) with zero.
"""

import numpy as np

def transform(input_grid):
    # Get Dimensions
    rows = len(input_grid)
    cols = len(input_grid[0])

    # Duplicate Pixels
    duplicated_grid = np.zeros((2 * rows, 2 * cols), dtype=int)
    for i in range(rows):
        for j in range(cols):
            value = input_grid[i][j]
            duplicated_grid[2*i][2*j] = value
            duplicated_grid[2*i+1][2*j] = value
            duplicated_grid[2*i][2*j+1] = value
            duplicated_grid[2*i+1][2*j+1] = value

    # Add Padding
    output_grid = np.zeros((2 * rows + 2, 2 * cols + 2), dtype=int)
    output_grid[1:2*rows+1, 1:2*cols+1] = duplicated_grid

    return output_grid