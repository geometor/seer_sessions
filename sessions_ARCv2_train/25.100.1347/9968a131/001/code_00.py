"""
Transforms an input grid by performing a right circular shift on the elements of 
all odd-indexed rows (1, 3, 5, ...). Even-indexed rows remain unchanged.
A right circular shift moves the last element of the row to the first position, 
and all other elements shift one position to the right.
"""

import numpy as np # Using numpy for efficient array manipulation, specifically np.roll

def _circular_shift_right(row: list[int]) -> list[int]:
    """
    Performs a right circular shift on the elements of a list.
    
    Args:
        row: The list of integers to be shifted.
        
    Returns:
        A new list with elements shifted one position to the right, circularly.
    """
    if not row:
        return []
    # Alternative implementation without numpy:
    # return [row[-1]] + row[:-1] 
    
    # Using numpy for potential efficiency with larger arrays
    np_row = np.array(row)
    shifted_row = np.roll(np_row, 1)
    return shifted_row.tolist()

def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of lists representing the 2D grid of integers.

    Returns:
        A new list of lists representing the transformed grid.
    """
    # Initialize output_grid as an empty list
    output_grid = []

    # Iterate through each row of the input grid along with its index
    for i, row in enumerate(input_grid):
        # Check if the current row index 'i' is odd (1, 3, 5, ...)
        if i % 2 == 1:
            # If the index is odd, perform a right circular shift on the row
            shifted_row = _circular_shift_right(row)
            # Append the shifted row to the output grid
            output_grid.append(shifted_row)
        else:
            # If the index is even (0, 2, 4, ...), keep the row unchanged
            # Append a copy of the original row to ensure the input_grid is not modified
            output_grid.append(row[:]) 

    # Return the final transformed grid
    return output_grid