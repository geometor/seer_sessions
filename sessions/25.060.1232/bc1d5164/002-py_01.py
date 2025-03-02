"""
The transformation extracts a recurring 3x3 block of non-zero pixels from the input grid and uses this to create new 3x3 output array.
"""

import numpy as np

def get_non_zero_positions(grid):
    """
    Finds the positions of non-zero elements in the input grid.
    """
    rows, cols = np.where(grid != 0)
    return list(zip(rows, cols))


def transform(input_grid):
    """
    Transforms the input grid by extracting the 3x3 pattern of non-zero pixels.
    """
    input_grid = np.array(input_grid)  # Convert to numpy array for easier manipulation

    # 1. Identify Non-zero Pixels and Their Positions
    non_zero_positions = get_non_zero_positions(input_grid)

    # 2. Determine Repeating Pattern & 3. Condense Rows and 4. Condense Columns
    # Find the bounding box of the non-zero elements.  We are implicitly looking for a 3x3 pattern

    output_grid = np.zeros((3, 3), dtype=int)

    if not non_zero_positions:
        return output_grid.tolist()
    
    # Extract non-zero subarray and wrap into 3x3
    first_row = non_zero_positions[0][0]
    first_col = non_zero_positions[0][1]
    
    for i in range(3):
      for j in range(3):
        row = first_row + i
        col = first_col + j
        if row < input_grid.shape[0] and col < input_grid.shape[1]:
          if input_grid[row, col] !=0:
            output_grid[i,j] = input_grid[row, col]

    return output_grid.tolist()