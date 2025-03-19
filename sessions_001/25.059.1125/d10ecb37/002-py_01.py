"""
Extracts the top-left 2x2 subgrid from the input grid and returns it as the output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Extracts the top-left 2x2 subgrid of the input.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The 2x2 output grid.
    """
    # Convert the input grid to a NumPy array for easier slicing.
    input_array = np.array(input_grid)

    # Extract the top-left 2x2 subgrid.
    output_array = input_array[:2, :2]

    # Convert the NumPy array back to a list of lists.
    output_grid = output_array.tolist()

    return output_grid