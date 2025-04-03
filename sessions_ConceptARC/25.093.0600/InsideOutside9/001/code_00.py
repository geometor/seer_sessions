"""
The transformation identifies boundary lines defined by the locations of the number 2. 
It determines whether these boundaries are primarily horizontal (rows) or vertical (columns) based on which dimension (row index or column index) has fewer unique values among the cells containing 2. 
Then, it filters the number 4s in the grid. Only 4s located strictly between the minimum and maximum boundary indices (along the determined orientation) are kept. 
All other 4s are changed to 0s. Numbers 0 and 2 remain unchanged.
"""

import numpy as np

def find_boundary_indices(grid, value):
    """Finds the row and column indices of cells containing the specified value."""
    locations = np.argwhere(grid == value)
    if locations.size == 0:
        return [], [] # No value found
    rows = np.unique(locations[:, 0])
    cols = np.unique(locations[:, 1])
    return rows, cols

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input to numpy array for easier processing
    input_array = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_array)

    # Locate all cells containing the boundary value '2'
    rows_2, cols_2 = find_boundary_indices(input_array, 2)

    # Handle cases where no '2's are found (return copy of input)
    if len(rows_2) == 0 and len(cols_2) == 0:
         return output_grid.tolist() # No boundaries defined

    # Determine the boundary orientation and find min/max indices
    min_idx = -1
    max_idx = -1
    orientation = 'column' # Default to column if counts are equal or no rows found

    # Check if row orientation is more dominant (fewer unique rows than columns)
    if len(rows_2) > 0 and (len(cols_2) == 0 or len(rows_2) < len(cols_2)):
        orientation = 'row'
        min_idx = np.min(rows_2)
        max_idx = np.max(rows_2)
    # Check if column orientation is dominant or equally dominant
    elif len(cols_2) > 0 : # Handles len(cols_2) <= len(rows_2) including equality
        orientation = 'column'
        min_idx = np.min(cols_2)
        max_idx = np.max(cols_2)
    # else: # Should not happen if the first check passes for rows_2 > 0, but covers edge cases
    #    return output_grid.tolist() # No clear orientation if only one '2' exists? Example implies clear lines.

    # Find locations of the target value '4'
    rows_4, cols_4 = np.where(input_array == 4)

    # Iterate through each cell containing '4'
    for r, c in zip(rows_4, cols_4):
        keep_4 = False
        # Check if the '4' is within the boundaries based on orientation
        if orientation == 'row':
            if min_idx < r < max_idx:
                keep_4 = True
        elif orientation == 'column':
             if min_idx < c < max_idx:
                keep_4 = True

        # If the '4' is not strictly between the boundaries, change it to '0'
        if not keep_4:
            output_grid[r, c] = 0

    # Convert the result back to a list of lists
    return output_grid.tolist()
