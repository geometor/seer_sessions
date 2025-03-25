"""
Iterate through each pixel of the input grid. Identify red (2) pixels.
If a red pixel is in the bottom half of the grid, and is not in the first or last column, 
and the sum of its row and column indices is even, replace it with azure (8).
Otherwise, keep the original color. Output the modified grid.
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
                # Check if the pixel is in the bottom half, not on edges, and has even row+col sum
                if i >= rows // 2 and j > 0 and j < cols -1 and (i + j) % 2 == 0:
                    output_grid[i, j] = 8  # Replace with azure (8)
    
    return output_grid