"""
1.  **Identify Diagonals**: Locate the main diagonal (top-left to bottom-right) and the anti-diagonal (top-right to bottom-left) of the input grid.
2.  **Main Diagonal**: If a pixel is on the main diagonal, change the color to orange (7).
3. **Anti-Diagonal**: If a pixel is on the anti-diagonal, change the color to orange (7).
4. **Other Elements**: Set all other pixels (not on the main diagonal or anti-diagonal), change color to black (0).
"""

import numpy as np

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.zeros_like(input_grid)
    rows, cols = output_grid.shape

    # Iterate over each pixel in the grid
    for i in range(rows):
        for j in range(cols):
            # Main Diagonal: Change the main diagonal element color to orange (7)
            if i == j:
                output_grid[i, j] = 7
            # Anti-Diagonal: Change the anti-diagonal color to orange (7).
            elif i + j == rows - 1:
                output_grid[i, j] = 7
            # Other Elements: Set other elements not on main or anti-diagonal to black(0).
            else:
                output_grid[i,j] = 0

    return output_grid