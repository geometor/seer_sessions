"""
1.  **Input:** A grid of arbitrary size (but at least 4x4).
2.  **Output:** A 4x4 grid.
3.  **Transformation:** The output grid is a 4x4 subgrid extracted from the input grid. The subgrid's location within the input grid is *not* fixed and must be determined by analyzing the relationship between the specific input and output grids in each example. The subgrids in all the examples except example 5 have the colors 0,1,4,9, however example 5 breaks this since the valid colors are 0,1 and 4. The background of the input surrounding the subgrid is always color 2.
"""

import numpy as np

def find_subgrid(input_grid):
    """
    Finds the 4x4 subgrid within the input grid.
    Iterates through all possible 4x4 subgrids and checks for a potential match
    based on the background color (2) surrounding the subgrid.
    """
    input_rows, input_cols = input_grid.shape
    for r in range(input_rows - 3):
        for c in range(input_cols - 3):
            subgrid = input_grid[r:r+4, c:c+4]
            # Check if the subgrid might be the correct one by examining its surroundings.
            if is_potential_subgrid(input_grid, r, c):
                return subgrid
    return None

def is_potential_subgrid(input_grid, r, c):
    """
    Checks if the 4x4 subgrid at position (r, c) is a potential match by
    examining the surrounding pixels for the background color (2).
    This isn't foolproof, but provides a heuristic based on the observation
    that the background around the subgrid is often color 2.
    """
    input_rows, input_cols = input_grid.shape

    # Check top border (excluding corners)
    if r > 0:
        for i in range(c + 1, c + 3):
            if i < input_cols and input_grid[r-1, i] != 2:
                return False

    # Check bottom border (excluding corners)
    if r + 4 < input_rows:
        for i in range(c + 1, c + 3):
            if i < input_cols and input_grid[r+4, i] != 2:
                return False

    # Check left border (excluding corners)
    if c > 0:
        for i in range(r + 1, r + 3):
            if input_grid[i, c-1] != 2:
                return False

    # Check right border (excluding corners)
    if c + 4 < input_cols:
       for i in range(r + 1, r + 3):
            if input_grid[i, c+4] != 2:
              return False

    return True

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    
    # Find and extract subgrid
    output_grid = find_subgrid(input_grid)

    if output_grid is None: # Fallback if our check does not find the subgrid
      output_grid = np.zeros((4,4), dtype=int) #Return 0s grid

    return output_grid.tolist()