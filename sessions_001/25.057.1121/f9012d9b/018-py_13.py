"""
1.  **Identify Target Region:** Locate a 2x1 region of *identical* color, vertically oriented, within the input grid.
2.  **Extract 2x2 Region:** Create a 2x2 region using the identified 2x1 region as the left side, and the two adjacent pixels on the right as the right side.
3.  **Output:** The output is this constructed 2x2 region.
4. If no 2x1 vertical region is found return an empty grid.
"""

import numpy as np

def find_vertical_2x1_region(grid):
    """Finds the first 2x1 region of identical pixels, vertically oriented."""
    rows, cols = grid.shape
    for r in range(rows - 1):
        for c in range(cols):
            if grid[r, c] == grid[r+1, c]:
                return r, c
    return None  # Return None if no 2x1 vertical region is found

def get_subgrid(grid, row_start, col_start, size):
    """Extracts a subgrid of specified size from the given grid."""
    return grid[row_start:row_start+size, col_start:col_start+size]

def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    
    # Find the first 2x1 vertical region of identical color
    coords = find_vertical_2x1_region(input_grid)
    
    if coords is not None:
        row, col = coords
        # Check if we can extract a 2x2 region (stay within bounds)
        if col + 1 < input_grid.shape[1]:
          output_grid = get_subgrid(input_grid, row, col, 2)
        else: # if the 2x1 is on the edge, return empty.
          output_grid = np.array([[]])
    else:  # Handle the case where no 2x1 vertical region is found
        output_grid = np.array([[]])
    
    return output_grid.tolist()