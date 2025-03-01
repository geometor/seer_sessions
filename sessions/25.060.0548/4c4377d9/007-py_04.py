"""
1.  **Identify the row containing two adjacent white (0) pixels.** This is the target row.
2.  **Duplicate the target row.**
3.  **Insert the duplicated row into the grid.** The insertion point appears to be *before* the last row of the input grid. This effectively makes the original last row to be inserted *after* the duplicated row.
4. The input is expanded by inserting the original last row *before* the duplicated last row, and also inserting a copy of the row with the white pixels at the row location of the input grid.
"""

import numpy as np

def find_row_with_adjacent_whites(grid):
    """Finds the index of the row with two adjacent white (0) pixels."""
    for i, row in enumerate(grid):
        for j in range(len(row) - 1):
            if row[j] == 0 and row[j+1] == 0:
                return i
    return -1  # Should not happen in this task, but good practice.

def transform(input_grid):
    # Convert the input grid to a NumPy array.
    input_array = np.array(input_grid)
    rows, cols = input_array.shape

    # Find the row with adjacent white pixels.
    target_row_index = find_row_with_adjacent_whites(input_grid)

    # Duplicate the target row.
    duplicated_row = input_array[target_row_index, :].copy()

    # create output grid with space for added rows
    output_array = np.zeros((rows + 1, cols), dtype=int)

    #copy all rows up to target row
    output_array[:target_row_index+1,:] = input_array[:target_row_index+1,:]
    
    # add dup row
    output_array[target_row_index+1,:] = duplicated_row

    # Copy remaining, skip target row
    output_array[target_row_index+2:,:] = input_array[target_row_index+1:,:]


    # Convert the NumPy array back to a list.
    output_grid = output_array.tolist()
    
    return output_grid