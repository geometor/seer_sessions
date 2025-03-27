"""
The transformation rule identifies vertically repeating patterns in the input grid and extracts the last occurrence of the repeating pattern as the output grid.
"""

import numpy as np

def find_repeating_subgrid(grid):
    """
    Finds the smallest repeating subgrid pattern vertically.
    """
    rows, cols = grid.shape
    for subgrid_height in range(1, rows + 1):
        if rows % subgrid_height == 0:
            subgrid = grid[:subgrid_height]
            repeats = rows // subgrid_height
            valid_repeat = True
            for i in range(1, repeats):
                start_row = i * subgrid_height
                end_row = start_row + subgrid_height
                if not np.array_equal(grid[start_row:end_row], subgrid):
                    valid_repeat = False
                    break
            if valid_repeat:
                return subgrid
    return grid # If no repetition, just assume entire grid

def transform(input_grid):
    """
    Identifies the repeating subgrid pattern and returns the last one.
    """
    # Convert to numpy array for easier manipulation
    input_grid = np.array(input_grid)

    # Find repeating subgrid
    repeating_subgrid = find_repeating_subgrid(input_grid)

    # The last instance of the repeating pattern is the output
    output_grid = repeating_subgrid

    return output_grid.tolist()