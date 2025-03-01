"""
Replicates the input grid horizontally four times, adds three empty columns, replicates the input grid vertically five times, and fills the remaining cells with 0.
"""

import numpy as np

def transform(input_grid):
    # Create an output grid of size 15x15, initialized with 0s.
    output_grid = np.zeros((15, 15), dtype=int)

    # Replicate the input grid horizontally four times.
    for i in range(4):
      output_grid[:3, i*3:(i+1)*3] = input_grid

    # Add three columns.
    output_grid[:3, 12:15] = np.zeros((3,3), dtype=int)
    
    # Replicate vertically. Input grid occupies only three rows.
    for i in range(3):
        output_grid[i, : ] = output_grid[i % 3, :]
    
    #The rest is already zero.

    return output_grid