import numpy as np

"""
Transforms the input 2D grid (containing a single row) by shifting the initial contiguous block of non-white pixels one position to the right within that row. 
The first element of the row becomes white (0), and the last element of the original row is effectively discarded to maintain the row length. 
The output grid retains the original shape (1 row, N columns).
"""

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the right-shift transformation to the single row of the input grid.

    Args:
        input_grid (np.ndarray): A 2D numpy array, expected shape (1, N).

    Returns:
        np.ndarray: The transformed 2D numpy array with the same shape as the input.
    """
    # Verify input shape (optional but good practice for ARC)
    if input_grid.shape[0] != 1:
        # This case shouldn't occur based on the examples, but handles potential variation
        # For now, we'll assume the input always matches the observed pattern.
        # In a more complex scenario, error handling or different logic might be needed.
        pass 

    # Extract the first (and only) row
    input_row = input_grid[0]
    
    # Get the length (number of columns) of the row
    num_cols = len(input_row)

    # Create the output row, initialized with white (0)
    # Using np.zeros ensures the correct data type
    output_row = np.zeros(num_cols, dtype=input_row.dtype) 

    # Perform the shift:
    # Copy elements from index 0 to N-2 of the input row
    # to index 1 to N-1 of the output row.
    # The first element (index 0) of output_row remains 0.
    # The last element (index N-1) of input_row is effectively dropped.
    if num_cols > 1: # Avoid index error for 1x1 grids (though unlikely here)
      output_row[1:] = input_row[:-1]
    # If num_cols is 1, output_row is already [0], which is correct for a 1x1 shift.

    # Reshape the output row back into a 2D grid with one row
    # This ensures the output format matches the input format
    output_grid = output_row.reshape(1, num_cols)

    return output_grid