"""
The transformation rule depends on the specific characteristics of the input grid. There are at least three different transformations observed:

1. If the input grid contains duplicate rows, only keep the first occurrence of each unique row.
2. If the input grid is square, transpose it (swap rows and columns).
3. If the input grid's non-zero values only occur on the main diagonal (and the grid is not modified by rule 1), keep the input grid as is.
4.  If all rows are identical, consolidate into a single row.

This suggests a conditional transformation based on input properties.
"""

import numpy as np

def _is_square(grid):
    """Checks if a grid is square."""
    return grid.shape[0] == grid.shape[1]

def _transpose(grid):
    """Transposes a grid."""
    return grid.T

def _unique_rows(grid):
    """Returns unique rows of a grid, preserving order."""
    output_grid = []
    seen_rows = []

    # Iterate through rows
    for row in grid:
        row_list = row.tolist()
        if row_list not in seen_rows:
            output_grid.append(row_list)
            seen_rows.append(row_list)

    return np.array(output_grid)

def _all_rows_identical(grid):
    """Checks if all rows in the grid are identical."""
    if len(grid) == 0:
        return True
    first_row = grid[0].tolist()
    for row in grid:
        if row.tolist() != first_row:
            return False
    return True

def _consolidate_identical_rows(grid):
    """Consolidates identical rows into a single row."""
    return np.array([grid[0]])

def _only_diagonal_nonzero(grid):
    """Checks if non-zero values are present only on the main diagonal"""
    rows, cols = grid.shape
    for i in range(rows):
        for j in range(cols):
            if i != j and grid[i, j] != 0:
                return False
    return True

def transform(input_grid):
    """
    Applies different transformations based on input grid properties.
    """
    # Check for all rows identical condition first
    if _all_rows_identical(input_grid):
        return _consolidate_identical_rows(input_grid)
    
    # Check for unique row condition
    temp_grid = _unique_rows(input_grid)
    if not np.array_equal(temp_grid, input_grid):
          return temp_grid
        
    # Check if the grid is square
    if _is_square(input_grid):
        #Check for unique rows, as unique rows takes precedence.
        
        # if not, Check if the nonzero values are only present on the main diagonal.
        if _only_diagonal_nonzero(input_grid):
            return input_grid
      
        return _transpose(input_grid)
    
    #Return unique rows by default
    return _unique_rows(input_grid)