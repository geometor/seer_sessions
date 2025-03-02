"""
The transformation rotates a specific 2x2 subgrid within the input grid by 90 degrees clockwise. The subgrid to be rotated is identified by having the color 8 (azure) in its top-left cell. If no such subgrid is found, the input grid remains unchanged.

1.  **Identify Potential Subgrids:** Examine all possible 2x2 subgrids within the input grid.
2.  **Locate Target Subgrid:** Find the 2x2 subgrid where the top-left cell is color 8 (azure).
3.  **Handle Absence:** If no such subgrid exists, the output is identical to the input.
4.  **Rotate:** If the target subgrid is found, rotate it 90 degrees clockwise.
    *   The top-left cell moves to the top-right position.
    *   The top-right cell moves to the bottom-right position.
    *   The bottom-right cell moves to the bottom-left position.
    *   The bottom-left cell moves to the top-left position.
5.  **Preserve Rest:** All other pixels in the grid that are not part of the rotating subgrid remain unchanged.
"""

import numpy as np

def rotate_subgrid(grid, top_left_row, top_left_col):
    """Rotates a 2x2 subgrid 90 degrees clockwise."""
    subgrid = grid[top_left_row:top_left_row+2, top_left_col:top_left_col+2]
    rotated_subgrid = np.rot90(subgrid, k=-1)  # k=-1 for clockwise rotation
    grid[top_left_row:top_left_row+2, top_left_col:top_left_col+2] = rotated_subgrid
    return grid

def find_target_subgrid(grid):
    """Finds the 2x2 subgrid with 8 (azure) in the top-left cell."""
    for r in range(grid.shape[0] - 1):
        for c in range(grid.shape[1] - 1):
            if grid[r, c] == 8:
                return r, c
    return None, None  # Return None if not found

def transform(input_grid):
    """Transforms the input grid by rotating the 2x2 subgrid with 8 in the top-left corner."""
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    # Find top-left corner of sub-grid
    top_left_row, top_left_col = find_target_subgrid(output_grid)

    # Rotate the identified subgrid if it exist
    if top_left_row is not None and top_left_col is not None:
       output_grid = rotate_subgrid(output_grid, top_left_row, top_left_col)

    return output_grid