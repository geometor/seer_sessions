"""
1.  **Identify White Pixels:** Locate all pixels within the input grid that have a value of 0 (representing the color white).

2.  **Conditional Color Transformation (Parity-Based):** For each identified white pixel, determine the parity (evenness or oddness) of its row index (`i`) and column index (`j`). Apply the following transformation rules:

    *   If *both* `i` and `j` are even, replace the white pixel with the color red (value 2).
    *   If *both* `i` and `j` are odd, replace the white pixel with the color green (value 3).
    *   If `i` is even and `j` is odd, replace the white pixel with the color blue (value 1).
    *   If `i` is odd and `j` is even, replace the white pixel with the color blue (value 1).

3.  **Preservation of Non-White Pixels:** All pixels in the original input grid that are *not* white (i.e., have values other than 0) remain unchanged in the output grid.

4.  **Output:** The final output is a new grid where all identified transformations have been implemented.
"""

import numpy as np

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # change output pixels
    for i in range(rows):
        for j in range(cols):
            if input_grid[i, j] == 0:  # If the pixel is white
                # Conditional replacement based on row/column parity
                if i % 2 == 0 and j % 2 == 0:
                    output_grid[i, j] = 2  # Red
                elif i % 2 != 0 and j % 2 != 0:
                    output_grid[i, j] = 3  # Green
                elif i % 2 == 0 and j % 2 != 0:
                    output_grid[i, j] = 1  # Blue
                elif i % 2 != 0 and j % 2 == 0:
                    output_grid[i, j] = 1  # Blue

    return output_grid