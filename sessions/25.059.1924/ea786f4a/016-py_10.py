"""
1. **Find the Center:** Locate the center pixel of the input grid. In this 7x7 grid, the center is at coordinates (3, 3) (zero-indexed).
2.  **Propagate the Center Color:** Change the color of every pixel that lies on either the same row, or the same column of the central pixel to the color of the central pixel.
3. All other pixels remain unchanged.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # find the center coordinates
    center_row = rows // 2
    center_col = cols // 2

    # get center pixel color
    center_color = input_grid[center_row, center_col]
    
    # change output pixels 
    for i in range(rows):
        output_grid[i, center_col] = center_color  # change pixels on central column
    for j in range(cols):
        output_grid[center_row, j] = center_color  # change pixels on central row
    
    return output_grid