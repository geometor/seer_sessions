import copy
import numpy as np # Although not strictly needed for the logic, import if the environment uses numpy arrays

"""
Transforms the input grid by filling zero cells downwards within each column. 
If a cell contains zero, its value in the output grid is replaced by the value 
of the nearest non-zero cell found directly above it in the same column of the 
input grid. If there are no non-zero cells above a zero cell in its column, 
it remains zero. Non-zero cells retain their original value in the output.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the downward fill transformation to the input grid.

    Args:
        input_grid: A list of lists representing the input grid of integers.

    Returns:
        A list of lists representing the transformed grid.
    """
    # Convert to list of lists if input is numpy array, for consistent handling
    if isinstance(input_grid, np.ndarray):
        input_list_grid = input_grid.tolist()
    else:
        input_list_grid = input_grid

    # Handle empty input grid
    if not input_list_grid or not input_list_grid[0]:
        return []

    # Get grid dimensions
    rows = len(input_list_grid)
    cols = len(input_list_grid[0])

    # Initialize output_grid as a deep copy of the input grid to avoid modifying the original
    output_grid = copy.deepcopy(input_list_grid)

    # Iterate through each column
    for c in range(cols):
        # This variable stores the last non-zero value encountered while moving down the current column
        last_non_zero_value = 0
        
        # Iterate through each row in the current column, from top to bottom
        for r in range(rows):
            # Get the value from the *original* input grid for logic checks
            current_input_value = input_list_grid[r][c]

            # Check if the cell in the original input grid is non-zero
            if current_input_value != 0:
                # If it's non-zero, update the value that should propagate downwards
                last_non_zero_value = current_input_value
            # Else, if the cell in the original input grid is zero *and* we have previously found a non-zero value above it
            elif last_non_zero_value != 0:
                # Update the corresponding cell in the output grid with the propagating value
                output_grid[r][c] = last_non_zero_value
                
    # Return the modified grid
    return output_grid
