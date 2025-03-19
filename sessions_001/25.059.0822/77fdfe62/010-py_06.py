"""
1. **Locate Corner Pixels:** Identify the pixel values at the four corners of the input grid:
    *   Top-left: (row 0, column 0)
    *   Top-right: (row 0, column 5)
    *   Bottom-left: (row 5, column 0)
    *    Bottom-right: (row 5, column 3)
2.  **Construct Output Grid:** Create a 2x2 output grid. Populate it with the values obtained in step 1, maintaining their relative positions:
    *   Output grid (0, 0) = Input grid (0, 0)
    *   Output grid (0, 1) = Input grid (0, 5)
    *   Output grid (1, 0) = Input grid (5, 0)
    *   Output grid (1,1) = Input grid (5,3)
"""

import numpy as np

def transform(input_grid):
    """Transforms an input grid by extracting the corner elements into a 2x2 output grid."""

    # Get input grid dimensions.
    rows = len(input_grid)
    cols = len(input_grid[0])
    
    # Initialize the output grid as a 2x2 numpy array.
    output_grid = np.zeros((2, 2), dtype=int)

    # Extract the corner values from the input grid.
    output_grid[0, 0] = input_grid[0][0]          # Top-left
    output_grid[0, 1] = input_grid[0][cols - 1]   # Top-right
    output_grid[1, 0] = input_grid[rows - 1][0]   # Bottom-left
    output_grid[1, 1] = input_grid[rows-1][3] # Bottom-right

    return output_grid