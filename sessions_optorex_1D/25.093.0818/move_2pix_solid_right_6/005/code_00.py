import numpy as np
import math

"""
The transformation rule takes a 2D NumPy array (grid) with one row and N columns.
It identifies a contiguous horizontal block of a single non-zero digit within that row.
This entire block is then shifted two positions (columns) to the right.
The positions in the output grid corresponding to the new block location are filled 
with the non-zero digit, while all other positions remain zero. The grid dimensions 
remain constant. Boundary conditions apply: if the shift moves part of the block 
beyond the right edge of the grid, that part is clipped.
"""

def _find_non_zero_block_indices_2d(grid: np.ndarray) -> tuple[int | None, int, int]:
    """
    Finds the non-zero value and the start/end column indices of its 
    contiguous block within the first row of the grid.
    
    Args:
        grid: The input 2D NumPy array (assumed shape (1, N)).
        
    Returns:
        A tuple containing:
        - The non-zero value (or None if all zeros).
        - The starting column index of the block (or -1 if not found).
        - The ending column index of the block (or -1 if not found).
    """
    # Ensure we are working with the first row
    if grid.shape[0] != 1:
        # Handle unexpected input shape if necessary, or raise error
        # For now, assume correct input shape based on examples
        pass 
        
    row_array = grid[0, :]
    
    # Find column indices of non-zero elements in the first row
    non_zero_col_indices = np.where(row_array != 0)[0]

    # Handle case where the row is all zeros
    if len(non_zero_col_indices) == 0:
        return None, -1, -1

    # Get the non-zero value (assuming only one unique non-zero value exists per block)
    # Use the index of the first non-zero element found
    first_non_zero_col = non_zero_col_indices[0]
    non_zero_value = int(row_array[first_non_zero_col]) 
    
    # Find the start and end column index of the contiguous block
    start_col_index = np.min(non_zero_col_indices)
    end_col_index = np.max(non_zero_col_indices)
    
    # Optional: Add verification for contiguity if needed for more complex scenarios
    
    return non_zero_value, int(start_col_index), int(end_col_index)


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule: shifts the non-zero block 
    in the first row two steps right.

    Args:
        input_grid: The input 2D NumPy array (shape 1xN).

    Returns:
        The transformed 2D NumPy array (shape 1xN).
    """
    # Get the shape (number of rows, number of columns)
    if input_grid.ndim == 1:
        # Handle potential 1D input case gracefully if it might occur
        # Forcing it to 2D for consistency
        input_grid = input_grid.reshape(1, -1) 
        
    rows, cols = input_grid.shape
    
    # Initialize the output grid with zeros, matching input size and type
    output_grid = np.zeros_like(input_grid)

    # Find the non-zero block details (value, start column, end column)
    non_zero_value, start_col, end_col = _find_non_zero_block_indices_2d(input_grid)

    # If a non-zero block was found, perform the shift
    if non_zero_value is not None:
        # Define the shift amount
        shift = 2
        
        # Calculate the new start and end column indices
        new_start_col = start_col + shift
        new_end_col = end_col + shift

        # Populate the output grid with the shifted block
        # Iterate through the column indices where the block *should* be in the output
        for c in range(new_start_col, new_end_col + 1):
             # Check bounds: only write if the column index is valid for the output grid
             if 0 <= c < cols:
                 # Assign the non-zero value to the correct position in the first row
                 output_grid[0, c] = non_zero_value

    return output_grid