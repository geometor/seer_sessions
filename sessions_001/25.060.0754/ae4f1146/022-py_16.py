"""
Extracts a 3x3 subgrid from the input grid. The subgrid appears to be
chosen based on being in the top-left region containing non-white pixels.
"""

import numpy as np

def transform(input_grid):
    """
    Extracts a 3x3 subgrid from the input grid.
    """
    # Convert input_grid to a NumPy array for easier slicing
    input_array = np.array(input_grid)

    # Define the dimensions of the subgrid
    subgrid_height = 3
    subgrid_width = 3

    # Extract the 3x3 subgrid from rows 1-3, cols 2-4.
    output_grid = input_array[1:4, 2:5]

    return output_grid.tolist()