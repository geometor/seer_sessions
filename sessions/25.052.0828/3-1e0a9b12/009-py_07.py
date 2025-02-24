"""
The transformation involves moving all colored cells down to the bottom row, maintaining their original column positions. If a cell is already in the bottom row, it remains unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by moving all non-zero colored cells to the bottom row,
    while keeping cells already on the bottom row unchanged.
    """
    input_grid = np.array(input_grid)
    output_grid = np.zeros_like(input_grid)
    rows, cols = input_grid.shape

    # Iterate through each column
    for j in range(cols):
        # Find non-zero elements in the column
        non_zero_indices = np.nonzero(input_grid[:, j])[0]
        if non_zero_indices.size > 0:
          # Check what is at the bottom
          colored_cell = input_grid[non_zero_indices[-1],j]
          output_grid[rows-1,j]=colored_cell
          
    # Copy elements already at the bottom to the output grid
    for i in range(cols):
      if input_grid[rows-1,i]!=0:
        output_grid[rows-1,i]=input_grid[rows-1,i]

    return output_grid