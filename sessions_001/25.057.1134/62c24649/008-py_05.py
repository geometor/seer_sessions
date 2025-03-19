"""
The input grid is replicated symmetrically to produce the output grid. The dimensions of the input grid are doubled to determine the dimensions of the output grid. The original input is placed in the center of the output. The first and last rows/columns are replicated to top/bottom and left/right.
"""

import numpy as np

def transform(input_grid):
    # Get input grid dimensions
    input_rows, input_cols = input_grid.shape

    # Determine output grid dimensions (doubled)
    output_rows = input_rows * 2
    output_cols = input_cols * 2

    # Initialize output grid with zeros
    output_grid = np.zeros((output_rows, output_cols), dtype=int)
    
    # Copy the input grid to the center of the output grid
    output_grid[input_rows//2:input_rows//2 + input_rows, input_cols//2:input_cols//2 + input_cols] = input_grid

    # Replicate Rows: Copy first and last rows to the top and bottom.
    output_grid[0:input_rows//2, input_cols//2:input_cols//2 + input_cols] = input_grid[0:input_rows//2,:]
    output_grid[input_rows//2 + input_rows:, input_cols//2:input_cols//2+input_cols] = input_grid[input_rows//2:,:]
    
    # Replicate Columns: Copy first and last colums to the left and right.
    output_grid[input_rows//2:input_rows//2+input_rows, 0:input_cols//2] = input_grid[:, 0:input_cols//2]
    output_grid[input_rows//2:input_rows//2+input_rows,input_cols//2+input_cols:] = input_grid[:,input_cols//2:]

    # replicate corners:
    output_grid[0:input_rows//2, 0:input_cols//2] = input_grid[0:input_rows//2, 0:input_cols//2]
    output_grid[0:input_rows//2, input_cols//2+input_cols:] = input_grid[0:input_rows//2, input_cols//2:]
    output_grid[input_rows//2 + input_rows:, 0:input_cols//2] = input_grid[input_rows//2:, 0:input_cols//2]
    output_grid[input_rows//2 + input_rows:, input_cols//2 + input_cols:] = input_grid[input_rows//2:, input_cols//2:]
    
    return output_grid