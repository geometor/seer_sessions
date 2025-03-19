"""
The transformation identifies the sequence of non-zero pixels in the input grid and uses this sequence to fill the output grid in a checkerboard pattern.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by extending the non-zero values into a checkerboard pattern
    """
    # Convert input_grid to a NumPy array for easier manipulation
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # 1. Identify Non-Zero Values and Their Positions:
    non_zero_values = []
    non_zero_positions = []
    
    for r in range(rows):
        for c in range(cols):
            if input_grid[r,c] != 0:
                non_zero_values.append(input_grid[r, c])
                non_zero_positions.append((r,c))


    # 2 & 3. Checkerboard Fill using sequence:
    seq_length = len(non_zero_values)
    for r in range(rows):
        for c in range(cols):
            output_grid[r,c] = non_zero_values[(r+c) % seq_length]

    return output_grid.tolist()