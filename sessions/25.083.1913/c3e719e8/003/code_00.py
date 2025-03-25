"""
1.  Create a 9x9 canvas filled with zeros.
2.  Horizontal Replication with Overlap:
    - Create a grid by concatenating the Input three times horizontally.
    - Place this grid at Top of the Canvas.
    - Place this grid at Bottom of the Canvas.
3.  Vertical Replication with Overlap
    - Create a grid by concatenating the input three times vertically.
    - Place this grid at the Left of the Canvas.
    - Place this grid, starting from column 4, on the Canvas.
4.  Overlapping Rule: When there are two writes on the same cell. The cell from Vertical Replication wins.
"""

import numpy as np

def transform(input_grid):
    # Create a 9x9 canvas of zeros.
    output_grid = np.zeros((9, 9), dtype=int)

    # Horizontal Replication.
    horizontal_grid = np.concatenate([input_grid, input_grid, input_grid], axis=1)

    # Place horizontal grid at the top.
    output_grid[:input_grid.shape[0], :] = horizontal_grid

    # Place horizontal grid at the bottom.
    output_grid[9 - input_grid.shape[0]:, :] = horizontal_grid
    
    # Vertical Replication
    vertical_grid = np.concatenate([input_grid, input_grid, input_grid], axis=0)
    
    # Place the vertical grid at the left
    output_grid[:, :input_grid.shape[1]] = vertical_grid

    # Place vertical grid with offset.
    output_grid[:, input_grid.shape[1]:2*input_grid.shape[1]] = vertical_grid

    return output_grid