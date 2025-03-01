"""
1. **Locate Subgrid:** Scan the input grid to find the position of the 3x3 section.
2. **Extract Subgrid:** Extract the 3x3 section.
3. **Output:** The extracted 3x3 section is the output grid.
"""

import numpy as np

def find_3x3_subgrid(input_grid):
    """Helper function to locate the 3x3 subgrid within the input grid."""
    rows, cols = input_grid.shape
    for r in range(rows - 2):
        for c in range(cols - 2):
            subgrid = input_grid[r:r+3, c:c+3]
            return subgrid, r, c  # Return the subgrid and its top-left corner coordinates
    return None, -1, -1 # Indicate failure if no 3x3 region can be extracted

def transform(input_grid):
    # Locate the 3x3 subgrid.
    subgrid, r_start, c_start = find_3x3_subgrid(input_grid)

    # Check if a 3x3 subgrid was found
    if subgrid is not None:
      output_grid = subgrid
    else:
      output_grid = np.zeros((3, 3), dtype=int) # a default grid

    return output_grid