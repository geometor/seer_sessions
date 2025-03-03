"""
Rotate the input grid 90 degrees clockwise and then mirror the rotated grid along its vertical axis.
"""

import numpy as np

def transform(input_grid):
    # Convert the input list of lists to a NumPy array
    input_grid = np.array(input_grid)

    # Rotate the grid 90 degrees clockwise
    rotated_grid = np.rot90(input_grid, k=-1)  # k=-1 rotates 90 degrees clockwise

    # Mirror the rotated grid along its vertical axis (flip horizontally)
    output_grid = np.fliplr(rotated_grid)

    return output_grid.tolist()