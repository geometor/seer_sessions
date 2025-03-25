"""
Copies an input grid to an output grid, preserving the outer frame of '6' and '7' pixels. The seventh row and seventh column from the bottom and right, respectively, are replaced.
If those rows/columns had '7' they are replaced with '6', except if the position intersects with the outer frame.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid according to the observed rules.
    """
    input_grid = np.array(input_grid)  # Convert to NumPy array for easier manipulation
    rows, cols = input_grid.shape
    output_grid = np.copy(input_grid)  # Start with a copy of the input grid

    # 1. Copy the Frame (already done by copying the input_grid)

    # 2. & 3. Modify 7th Row/Column from bottom and right, respectively:
    for r in range(rows):
      for c in range(cols):
        if r == rows - 7 :
          if input_grid[r,c] == 7 and (c != 0 and c != cols -1) :
            output_grid[r,c] = 6
        if c == cols - 7:
          if input_grid[r,c] == 7 and (r != 0 and r != rows - 1):
            output_grid[r,c] = 6

    return output_grid.tolist() # Convert back to list for consistency with the ARC format