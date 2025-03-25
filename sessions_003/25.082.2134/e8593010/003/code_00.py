"""
1.  **Locate White Pixels:** Identify all pixels in the input grid with the value 0 (white).

2.  **Conditional Replacement:** For *each* white pixel:
    *   If the pixel's row index and column index are both even, replace it with the color red (2).
    *   If the pixel's row index and column index are both odd, replace it with the color green (3).
    *   If the pixel's row index and column index have different parity (one is even, the other is odd), replace it with the color blue (1).

3. **Preserve Other Pixels:** All other pixels (gray and other colors other than white) are not changed.

4.  **Output Grid:** The final output grid is constructed with the replaced white pixels and all other original pixels preserved.
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
                if (i % 2 == 0 and j % 2 == 0):
                    output_grid[i, j] = 2  # Red
                elif (i % 2 != 0 and j % 2 != 0):
                    output_grid[i, j] = 3  # Green
                else:
                    output_grid[i, j] = 1  # Blue

    return output_grid