"""
Iterate through each pixel of the input grid.
Identify pixels that are red (color value 2).
For each red pixel, check if it is located in the bottom half of the grid,
not in the first or last column, and if its row index and column index
have different parity (one is even and the other is odd).
If all conditions are true, change the pixel's color to azure (color value 8).
Output the modified grid.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid according to the rule described above."""
    
    rows, cols = input_grid.shape
    output_grid = np.copy(input_grid)  # Initialize output grid

    for i in range(rows):
        for j in range(cols):
            # Check if the pixel is red (2)
            if input_grid[i, j] == 2:
                # Check if the pixel is in the bottom half, not on edges, and has different row/col parity
                if i >= rows // 2 and j > 0 and j < cols - 1 and (i % 2 != j % 2):
                    output_grid[i, j] = 8  # Replace with azure (8)
    
    return output_grid