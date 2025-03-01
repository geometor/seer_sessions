"""
1.  Find the Topmost Blue Row: Locate the topmost row in the input grid that contains at least one blue (1) pixel.
2. Target Row: If the top most blue row is not row index `0`, then the target row will be one above. If it IS row index `0`, it remains row index `0`.
3.  Replace with Red:** Replace all cells of the target row with red (2).
"""

import numpy as np

def find_top_blue_row(grid):
    """Finds the topmost row index containing a blue pixel."""
    for i, row in enumerate(grid):
        if 1 in row:
            return i
    return -1  # Return -1 if no blue pixel is found

def transform(input_grid):
    """Transforms the input grid according to the rules."""
    grid = np.array(input_grid)  # Convert to NumPy array for easier manipulation
    output_grid = np.copy(grid) # copy to modify
    top_blue_row = find_top_blue_row(grid)

    # Determine the target row
    if top_blue_row != -1:
        target_row = top_blue_row
        if (top_blue_row > 0):
            target_row = top_blue_row - 1
    else: # if no blue found, return original
      return output_grid
    

    # Replace the entire target row with red (2)
    output_grid[target_row, :] = 2
    
    return output_grid.tolist() # return as list