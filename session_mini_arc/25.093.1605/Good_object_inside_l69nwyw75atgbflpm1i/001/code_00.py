import numpy as np
import copy

"""
Identify the input grid. Create a copy for the output. Identify the inner grid (excluding the border).
Repeatedly iterate through the inner grid from top-to-bottom, column by column. 
If a cell within the inner grid contains a non-zero value and the cell directly below it (also within the inner grid) contains a zero, copy the non-zero value into the zero cell below.
Continue these iterations until a full pass through the inner grid results in no changes.
Return the modified output grid.
"""

def transform(input_grid):
    """
    Applies a gravity-like transformation to the inner part of a grid.
    Non-zero numbers fall downwards into zero cells within each column of the inner grid.
    """
    # Convert input list of lists to a NumPy array for easier manipulation
    input_array = np.array(input_grid)
    # Create a copy to modify, preserving the original input
    output_array = input_array.copy()
    
    # Get grid dimensions
    rows, cols = output_array.shape
    
    # Define inner grid boundaries (assuming a border of width 1)
    inner_start_row = 1
    inner_end_row = rows - 1  # Exclusive index for slicing
    inner_start_col = 1
    inner_end_col = cols - 1  # Exclusive index for slicing

    # Loop until no changes are made in a full pass
    while True:
        changed_in_pass = False
        # Iterate through columns of the inner grid
        for c in range(inner_start_col, inner_end_col):
            # Iterate through rows of the inner grid from top towards bottom
            # Need to check cell (r) and the one below (r+1), so stop one row early
            for r in range(inner_start_row, inner_end_row - 1):
                current_cell_value = output_array[r, c]
                cell_below_value = output_array[r + 1, c]
                
                # Check if the current cell has a value and the cell below is empty (0)
                if current_cell_value != 0 and cell_below_value == 0:
                    # Apply the "fall" / propagation
                    output_array[r + 1, c] = current_cell_value
                    # Mark that a change occurred in this pass
                    changed_in_pass = True
                    
        # If no changes were made in this entire pass, the grid has stabilized
        if not changed_in_pass:
            break
            
    # Convert the NumPy array back to a list of lists format for the output
    output_grid = output_array.tolist()
    
    return output_grid
