"""
Extracts a 5x5 sub-grid from the input grid. The sub-grid is determined by 
identifying a region of interest, potentially based on color patterns or shapes.
In this specific case, we locate a region centered around an azure and green pattern.
"""

import numpy as np

def find_target_region_center(input_grid):
    # Find the center coordinates of the target 5x5 region.  This is a hard-coded
    # solution for this specific example, and will be generalized later.
    # Searches for a green '3' surrounded by azure '8' pixels.

    rows, cols = input_grid.shape
    for r in range(rows - 2):
        for c in range(cols - 2):
            if input_grid[r+1, c+1] == 3:  #green
                if input_grid[r,c] == 8 and input_grid[r,c+1] == 8 and input_grid[r, c+2] == 8:
                   if input_grid[r+1,c] == 8  and input_grid[r+1, c+2] == 8:
                      if input_grid[r+2,c] == 8 and input_grid[r+2,c+1] == 8 and input_grid[r+2, c+2] == 8:
                        return (r+1,c+1) # center of azure square.
    return None


def transform(input_grid):
    """
    Transforms the input grid by extracting a 5x5 subgrid centered at a specific target location.
    """
    input_grid = np.array(input_grid) # Ensure numpy array
    center = find_target_region_center(input_grid)
    
    if center is None:
      return None # Or some other default/error handling.
      
    row_center, col_center = center

    # Calculate the top-left corner of the 5x5 region
    row_start = row_center - 2
    col_start = col_center - 2

    # Extract the 5x5 sub-grid
    output_grid = input_grid[row_start:row_start + 5, col_start:col_start + 5]

    return output_grid.tolist() # Convert back to list