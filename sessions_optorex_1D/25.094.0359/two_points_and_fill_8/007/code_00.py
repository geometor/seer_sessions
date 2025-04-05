"""
Transforms an input 2D grid (assumed shape 1xN) by finding the first and last 
non-zero elements along the second axis (columns). It identifies the non-zero 
value and fills the segment between these first and last column indices (inclusive) 
in the corresponding row (row 0) of an output grid (initially zeros, same shape 
as input) with that non-zero value.
"""

import numpy as np

def _find_non_zero_fill_info(grid: np.ndarray) -> tuple:
    """
    Finds the non-zero digit, its fixed row index, and the start/end column indices.

    Args:
        grid (np.ndarray): The input 2D numpy array (assumed 1xN).

    Returns:
        tuple: (non_zero_digit, row_index, start_col_index, end_col_index)
               Returns (0, -1, -1, -1) if no non-zero elements are found.
               Assumes only one row contains non-zero elements if multiple rows exist.
    """
    # 1. Find the coordinates (row, col) of all non-zero elements.
    non_zero_coords = np.where(grid != 0)
    
    # 2. Check if any non-zero elements were found.
    if len(non_zero_coords[0]) == 0:
        return 0, -1, -1, -1 # No non-zero elements

    # 3. Extract row and column indices.
    row_indices = non_zero_coords[0]
    col_indices = non_zero_coords[1]
    
    # 4. Determine the fixed row index (assuming all non-zeros are in the same row).
    #    In the examples, this is always row 0.
    row_index = row_indices[0] 
    
    # 5. Find the minimum (start) and maximum (end) column indices.
    start_col_index = np.min(col_indices)
    end_col_index = np.max(col_indices)
    
    # 6. Identify the non-zero digit using the first found coordinate.
    non_zero_digit = grid[row_index, start_col_index] # Use start_col_index or any other valid col index
    
    return non_zero_digit, row_index, start_col_index, end_col_index

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input numpy grid.

    Args:
        input_grid (np.ndarray): A 2D numpy array of integers (typically 1xN).

    Returns:
        np.ndarray: A 2D numpy array representing the transformed grid.
    """
    
    # 1. Find the necessary information: non-zero digit, row index, start/end column indices.
    non_zero_digit, row_index, start_col, end_col = _find_non_zero_fill_info(input_grid)

    # 2. Initialize the output grid with zeros, preserving the input shape and dtype.
    output_grid = np.zeros_like(input_grid)

    # 3. Check if valid non-zero information was found (row_index != -1).
    if row_index != -1:
        # 4. Fill the segment in the output grid.
        # Access the specific row (row_index) and the slice of columns from start_col to end_col (inclusive).
        # Assign the non_zero_digit to this slice.
        output_grid[row_index, start_col : end_col + 1] = non_zero_digit
        
    # 5. Return the modified output grid.
    return output_grid