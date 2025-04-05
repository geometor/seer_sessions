"""
Transforms the input grid by swapping adjacent columns based on the parity of the index of the first column containing a non-zero value.
1. Find the index of the first column (leftmost) containing any non-zero value. If all columns are zero, consider the index to be 0.
2. If this index is odd, swap adjacent column pairs starting from index 1 (i.e., swap (1,2), (3,4), ...).
3. If this index is even (or all zeros), swap adjacent column pairs starting from index 0 (i.e., swap (0,1), (2,3), ...).
"""

import copy
# numpy is not strictly necessary for this logic but can be useful for grid operations
# import numpy as np 

def find_first_non_zero_col(grid):
    """
    Finds the index of the first column containing a non-zero value.
    Returns -1 if the grid is empty or all values are zero.
    """
    if not grid or not grid[0]:
        return -1 # Indicate empty or invalid grid

    num_rows = len(grid)
    num_cols = len(grid[0])

    for j in range(num_cols):
        for i in range(num_rows):
            if grid[i][j] != 0:
                return j  # Found the first non-zero column index
    
    return -1 # No non-zero values found

def transform(input_grid):
    """
    Applies the conditional column swapping transformation.

    Args:
        input_grid: A list of lists representing the input 2D grid.

    Returns:
        A list of lists representing the transformed 2D grid.
    """
    # Handle empty grid case
    if not input_grid or not input_grid[0]:
        return []

    num_rows = len(input_grid)
    num_cols = len(input_grid[0])
    
    # initialize output_grid as a deep copy to avoid modifying the input
    output_grid = copy.deepcopy(input_grid)

    # 1. Find the index of the first non-zero column
    first_nz_col_index = find_first_non_zero_col(input_grid)

    # 2. Determine the starting index for swapping
    # If no non-zero found (first_nz_col_index == -1), treat as even (start at 0)
    if first_nz_col_index != -1 and first_nz_col_index % 2 != 0:
        start_index = 1 # Start swapping from pair (1, 2)
    else:
        start_index = 0 # Start swapping from pair (0, 1)

    # 3. Apply Swaps
    # Iterate through the columns with a step of 2, starting from the determined index
    for j in range(start_index, num_cols - 1, 2):
        # The loop condition ensures j < num_cols - 1, so j+1 is always a valid index within the loop
        
        # Swap the entire contents of column j with column j+1
        for i in range(num_rows):
            # Swap elements in each row for the current pair of columns
            output_grid[i][j], output_grid[i][j+1] = output_grid[i][j+1], output_grid[i][j]

    # 4. Output
    return output_grid