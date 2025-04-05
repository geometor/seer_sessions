"""
Transforms a 2D NumPy grid by shifting all non-zero elements down by exactly 
one row. Creates a new grid of the same dimensions initialized with zeros. 
For each non-zero element in the input grid at position (row, col), its value 
is copied to position (row + 1, col) in the output grid, provided that 
row + 1 is within the grid boundaries. Elements shifted beyond the last row 
are discarded. Zero elements in the input remain zero in the output unless 
overwritten by a shifted non-zero value.
"""

import numpy as np

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Shifts non-zero elements of a 2D NumPy array down by one row.

    Args:
        input_grid: A 2D NumPy array representing the input state.

    Returns:
        A new 2D NumPy array of the same shape as the input, with non-zero
        elements shifted down by one row.
    """
    # Get the dimensions (number of rows, number of columns) of the input grid
    rows, cols = input_grid.shape
    
    # Initialize an output grid of the same dimensions with all zeros
    # This ensures that positions not receiving a shifted value remain zero.
    output_grid = np.zeros_like(input_grid)

    # Iterate through each cell (row by row, then column by column) of the input grid
    for r in range(rows):
        for c in range(cols):
            # Check if the current cell contains a non-zero value
            if input_grid[r, c] != 0:
                # Calculate the target row index for the downward shift
                target_r = r + 1
                # The target column index remains the same
                target_c = c
                
                # Check if the target row index is still within the grid's boundaries
                # (i.e., less than the total number of rows)
                if target_r < rows:
                    # If the target position is valid, copy the non-zero value
                    # from the input grid to the corresponding position in the output grid.
                    output_grid[target_r, target_c] = input_grid[r, c]
            # If input_grid[r, c] is 0, no action is needed as output_grid is initialized with zeros.
            # If a non-zero element is shifted off the bottom edge (target_r >= rows), 
            # it's implicitly discarded because it's not copied to the output_grid.

    # Return the newly created output grid with the shifted elements
    return output_grid