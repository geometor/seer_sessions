"""
1.  **Identify the Active Row:** Find the row in the input grid that contains non-zero digits.
2.  **Locate Non-Zero Digits:** Within the active row, identify the positions and values of all non-zero digits.
3. **Expansion**: For each non-zero digit, expand the pixel to the left and to the right, using the same value/color, such that the original colored pixel is in the center and there is a block of 5 of the same color.
4.  **Insert Separator:** Place a single '5' (grey pixel) in the grid at the mid-point between the end of one colour expansion and the beginning of the adjacent one.
5.  **Preserve Other Rows:** All other rows in the input grid remain unchanged in the output grid.
6. **Output** output the final grid.
"""

import numpy as np

def find_active_row(grid):
    # Iterate through rows and check for non-zero elements
    for i, row in enumerate(grid):
        if np.any(row != 0):
            return i
    return -1  # No active row found

def expand_pixels(row, active_row_index, input_grid):
    # Create a copy of the row to modify
    new_row = np.copy(row)
    # Find the indices of non-zero elements
    non_zero_indices = np.where(row != 0)[0]
    
    # Calculate the midpoint between non-zero colors
    if len(non_zero_indices)>1:
      midpoint = (non_zero_indices[-1] + non_zero_indices[0]) // 2 
      new_row[midpoint] = 5

    # Expand each non-zero element
    for i in range(len(non_zero_indices)):
      idx=non_zero_indices[i]

      if len(non_zero_indices)==1:
        new_row[idx-2:idx+3]=input_grid[active_row_index, idx]
      elif i==0:
        new_row[non_zero_indices[0]:midpoint]=input_grid[active_row_index, idx]
      else:
        new_row[midpoint+1:non_zero_indices[-1]+1]=input_grid[active_row_index, idx]

    return new_row

def transform(input_grid):
    # Convert input grid to a NumPy array for easier manipulation
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)

    # Find the active row index
    active_row_index = find_active_row(input_grid)

    # If no active row, return the original grid
    if active_row_index == -1:
        return output_grid

    # Get the active row
    active_row = input_grid[active_row_index]

    # Expand pixels in the active row
    output_grid[active_row_index] = expand_pixels(active_row, active_row_index, input_grid)
    

    return output_grid.tolist()