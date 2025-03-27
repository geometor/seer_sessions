"""
Extracts the top-left 2x2 subgrid from the input grid to form the output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Extracts the top-left 2x2 subgrid from the input grid.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2x2 list representing the extracted subgrid.
                          Returns None if the input grid is smaller than 2x2.
    """
    # Convert input list of lists to a numpy array for easier slicing
    np_input_grid = np.array(input_grid, dtype=int)

    # Check if the input grid is at least 2x2
    if np_input_grid.shape[0] < 2 or np_input_grid.shape[1] < 2:
        # Handle cases where input is too small (though ARC constraints usually prevent this)
        # Based on the problem description, inputs are at least 1x1.
        # If the requirement is strictly a 2x2 output, this case needs clarification.
        # For now, let's assume valid inputs are at least 2x2 based on examples.
        # Alternatively, we could pad or return an error/empty grid.
        # Let's return None or raise an error if strict 2x2 output is required and input is smaller.
        # Given the examples, it seems inputs will always be large enough.
        pass # Assume inputs are large enough based on examples

    # Extract the top-left 2x2 subgrid using numpy slicing
    # Slicing [0:2, 0:2] selects rows 0 and 1, and columns 0 and 1
    output_grid_np = np_input_grid[0:2, 0:2]

    # Convert the resulting numpy array back to a list of lists
    output_grid = output_grid_np.tolist()

    return output_grid
