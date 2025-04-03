"""
Transforms the input 2D grid (assumed shape 1x12) by shifting its columns two 
positions to the left, discarding the first two columns, and appending two 
zero-filled columns at the end. The final output is a string of space-separated 
integers representing the transformed row.
"""

import numpy as np

def format_output(output_list):
  """Formats a list/array of numbers into a string of space-separated integers."""
  return ' '.join(map(str, output_list))

def transform(input_grid: np.ndarray) -> str:
    """
    Applies the left column shift and padding transformation to a 2D input grid.

    Args:
        input_grid: A 2D NumPy array, expected shape (1, 12).

    Returns:
        A string representation of the transformed sequence (the single row), 
        with elements separated by spaces.
    """
    # Define the number of columns to shift/discard from the left
    shift_amount = 2
    # Define the value to use for padding
    pad_value = 0

    # Ensure input is treated as 2D (specifically 1xN)
    # This handles cases where the input might be passed as 1D
    if input_grid.ndim == 1:
        input_grid = input_grid.reshape(1, -1)
    
    # Verify expected number of columns if needed (defensive programming)
    # num_rows, num_cols = input_grid.shape
    # if num_cols != 12:
    #     # Handle error: unexpected input shape
    #     raise ValueError(f"Expected input grid with 12 columns, got {num_cols}")

    # Select columns starting from index `shift_amount` to the end
    # This effectively discards the first `shift_amount` columns.
    # Slicing a 2D array like this preserves its 2D nature.
    shifted_part = input_grid[:, shift_amount:] # Shape will be (1, num_cols - shift_amount)

    # Create the 2D padding array with the correct shape (1, shift_amount)
    # Use the same data type as the input grid for consistency.
    padding = np.full((1, shift_amount), pad_value, dtype=input_grid.dtype) # Shape (1, shift_amount)

    # Concatenate the shifted part and the padding along the column axis (axis=1)
    output_grid_2d = np.concatenate((shifted_part, padding), axis=1) # Shape (1, num_cols)

    # Extract the single row from the 2D output grid to get a 1D array
    # flatten() or accessing the first row [0] both work
    output_sequence_1d = output_grid_2d.flatten() 

    # Format the resulting 1D NumPy array into a space-separated string
    output_str = format_output(output_sequence_1d)

    # Return the formatted string
    return output_str