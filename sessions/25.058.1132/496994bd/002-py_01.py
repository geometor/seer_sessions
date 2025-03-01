"""
The transformation vertically flips the contiguous block of non-white rows in the input grid to produce the output grid. The white rows act as padding or a background that remains unchanged.
"""

import numpy as np

def _find_non_white_region(grid):
    # Find the indices of the first and last non-white rows.
    rows, cols = grid.shape
    non_white_rows = []
    for i in range(rows):
        if np.any(grid[i] != 0):
            non_white_rows.append(i)
    if not non_white_rows:
        return 0, 0  # Handle the case where the entire grid is white
    start_row = non_white_rows[0]
    end_row = non_white_rows[-1] + 1
    return start_row, end_row

def transform(input_grid):
    """
    Vertically flips the non-white region of the input grid.
    """
    grid = np.array(input_grid)
    rows, cols = grid.shape
    output_grid = np.copy(grid)  # Initialize output grid

    # Find the non-white region
    start_row, end_row = _find_non_white_region(grid)

    # Extract and flip the region
    if start_row != end_row:
        non_white_region = grid[start_row:end_row]
        flipped_region = np.flipud(non_white_region)

        # Replace the region in the output grid
        output_grid[start_row:end_row] = flipped_region

        # Calculate the new position after flipping
        flipped_start_row = rows - end_row
        flipped_end_row   = rows - start_row
        output_grid[flipped_start_row:flipped_end_row] = flipped_region


    return output_grid.tolist()