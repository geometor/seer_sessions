"""
Rearrange the grid by systematically swapping adjacent pairs of columns.
Iterate through the columns starting from index 0, incrementing by 2.
For each index j, if column j+1 exists, swap column j with column j+1.
"""

import numpy as np
import copy

def swap_columns(grid, col1_idx, col2_idx):
    """
    Swaps two columns in a grid represented as a list of lists.
    """
    new_grid = copy.deepcopy(grid) # Work on a copy
    for row_idx in range(len(new_grid)):
        new_grid[row_idx][col1_idx], new_grid[row_idx][col2_idx] = \
            new_grid[row_idx][col2_idx], new_grid[row_idx][col1_idx]
    return new_grid

def transform(input_grid):
    """
    Applies the column swapping transformation to the input grid.

    Args:
        input_grid: A list of lists representing the input 2D grid.

    Returns:
        A list of lists representing the transformed 2D grid.
    """
    # Initialize output_grid as a deep copy of the input to avoid modifying the original
    output_grid = copy.deepcopy(input_grid)
    num_rows = len(output_grid)
    if num_rows == 0:
        return output_grid # Handle empty grid case
    num_cols = len(output_grid[0])

    # Iterate through the columns with a step of 2
    # We process pairs (0, 1), (2, 3), (4, 5), etc.
    for j in range(0, num_cols - 1, 2):
        # Check if the next column (j+1) exists
        # The range already ensures j < num_cols - 1, so j+1 is always a valid index within the loop
        
        # Swap the entire contents of column j with column j+1
        # Use a helper function for clarity or perform swap directly
        for i in range(num_rows):
            # Swap elements in each row for the current pair of columns
            output_grid[i][j], output_grid[i][j+1] = output_grid[i][j+1], output_grid[i][j]

    # The resulting grid after performing all necessary swaps is the output
    return output_grid
