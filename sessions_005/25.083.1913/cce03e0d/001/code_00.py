"""
The input 3x3 grid is replicated and placed into a 9x9 output grid. The positions of the replicas within the output grid are determined based on non-zero value and index inequality.
The rest of output grid filled with zeros.
"""

import numpy as np

def transform(input_grid):
    # Initialize a 9x9 output grid filled with zeros.
    output_grid = np.zeros((9, 9), dtype=int)

    # Get the dimensions of the input grid.
    input_rows, input_cols = input_grid.shape

    # Find positions in the input grid where the value is not zero AND row index != col index.
    non_zero_positions = [(x, y) for y, row in enumerate(input_grid) for x, value in enumerate(row) if value != 0 and x != y]


    # Calculate offset positions for insertion.
    offset_positions = [(3 * x, 3 * y) for x, y in non_zero_positions]

    # Place input grid replicas at determined positions.
    for x_offset, y_offset in offset_positions:
      if x_offset < output_grid.shape[1] and y_offset < output_grid.shape[0]:
        for i in range(input_rows):
            for j in range(input_cols):
                if  y_offset + i < output_grid.shape[0] and x_offset + j < output_grid.shape[1]:
                    output_grid[y_offset + i, x_offset + j] = input_grid[i, j]

    return output_grid