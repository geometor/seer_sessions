"""
Checks for the presence of the color blue (1) in the input grid. If found, the output is a 1x1 grid containing only the value 1.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid based on the presence of blue (1)."""

    # Convert input_grid to numpy array for easier processing
    input_grid = np.array(input_grid)

    # Check if the value 1 exists anywhere in the input grid
    if np.any(input_grid == 1):
        # If 1 is found, create a 1x1 output grid with the value 1
        output_grid = np.array([[1]])
    else:
        #  If no 1, based on ARC rules, a blank would not be correct, return
        #  all zeros
        output_grid = np.array([[0]])

    return output_grid