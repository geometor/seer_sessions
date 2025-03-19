"""
Extract the 2x2 inner block of non-blue pixels.
"""

import numpy as np

def find_non_blue_block(grid):
    """Finds the top-left corner of a 2x2 block of non-blue pixels."""
    rows, cols = grid.shape
    for r in range(rows - 1):
        for c in range(cols - 1):
            if (grid[r, c] != 1 and grid[r+1, c] != 1 and
                grid[r, c+1] != 1 and grid[r+1, c+1] != 1):
                return (r, c)
    return None

def transform(input_grid):
    """Extracts the 2x2 block of non-blue pixels."""
    
    # Convert input to numpy array for easier manipulation
    input_grid = np.array(input_grid)

    # Find the top-left corner of the 2x2 non-blue block
    top_left = find_non_blue_block(input_grid)

    # Extract the 2x2 block if found
    if top_left:
      r,c = top_left
      output_grid = input_grid[r:r+2,c:c+2]

    else:
        output_grid = np.array([]) # or some other default, depends on task req

    return output_grid.tolist()