"""
The transformation rule inserts blue (1) pixels to the immediate left and above of existing azure (8) colored objects, 
provided those positions were previously occupied by white pixels (0).
"""

import numpy as np

def get_azure_objects(grid):
    """
    Finds and returns the coordinates of all azure (8) pixels.
    """
    azure_coords = []
    for r_idx, row in enumerate(grid):
        for c_idx, pixel in enumerate(row):
            if pixel == 8:
                azure_coords.append((r_idx, c_idx))
    return azure_coords

def transform(input_grid):
    """
    Transforms the input grid according to the rule: insert '1' to the left and above '8' if '0'.
    """
    output_grid = np.copy(input_grid)
    azure_coords = get_azure_objects(input_grid)

    # Sort coordinates to process from top-left to bottom-right
    azure_coords.sort()

    for r, c in azure_coords:
        # Insert to the left
        if c > 0 and output_grid[r, c-1] == 0:
            output_grid[r, c-1] = 1
        # Insert above
        if r > 0 and output_grid[r-1, c] == 0:
            output_grid[r-1, c] = 1

    return output_grid