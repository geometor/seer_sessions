"""
The transformation rule is to reverse the order of rows in the input grid, 
pad to 3x3 if necessary, and then transpose the grid (swap rows and columns).
"""

import numpy as np

def transform(input_grid):
    # Reverse the order of rows.
    reversed_grid = input_grid[::-1]

    # Convert to numpy array for easier manipulation
    reversed_grid = np.array(reversed_grid)
    
    rows, cols = reversed_grid.shape

    # Pad with zeros to make it 3x3, if needed.
    if rows < 3 or cols < 3:
        padded_grid = np.zeros((3, 3), dtype=int)
        padded_grid[:rows,:cols] = reversed_grid
    else:
      padded_grid = reversed_grid

    # Transpose the grid.
    output_grid = padded_grid.T

    return output_grid.tolist()