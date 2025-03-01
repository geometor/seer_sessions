"""
1.  **Identify the White (0) Object:** Locate the contiguous block of white (0) pixels.
2.  **Find the Top-Left Corner of a 2x2 Output:** Find the top-left corner pixel for a 2x2 square. The top row should be all azure (8) and bottom row all white (0). The first white (0) pixel that can create such 2x2 block is at the top-left most corner.
3.  **Extract the Subgrid:** Extract the 2x2 subgrid based on the position found in the previous step.
"""

import numpy as np

def find_top_left_corner(grid):
    """Finds the top-left corner of the 2x2 subgrid."""
    rows, cols = grid.shape
    for r in range(rows - 1):
        for c in range(cols - 1):
            if grid[r, c] == 8 and grid[r, c+1] == 8 and grid[r+1,c] == 0 and grid[r+1,c+1] == 0:
                return r, c
    return None

def transform(input_grid):
    """Extracts a 2x2 subgrid based on the top-left corner of azure/white pattern."""
    # Convert input to numpy array
    input_grid = np.array(input_grid)

    # Find the top-left corner of the 2x2 subgrid
    start_row, start_col = find_top_left_corner(input_grid)

    # Extract the 2x2 subgrid
    output_grid = input_grid[start_row:start_row+2, start_col:start_col+2]

    return output_grid.tolist()