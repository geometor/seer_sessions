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

    # Check if the input grid is indeed 2D, handle potential 1D case gracefully
    # Although the error analysis suggests 2D, defensive coding is good.
    if input_grid.ndim == 1:
        # If somehow it's 1D, reshape to 1xN
        input_grid = input_grid.reshape(1, -1)
    elif input_grid.ndim != 2 or input_grid.shape[0] != 1:
        # Handle unexpected shapes if necessary, or raise an error
        # For this specific problem, we strongly expect (1, 12) based on examples and errors
        pass # Assuming correct shape (1, 12) based on prior analysis

    # Select columns starting from index `shift_amount` to the end
    # input_grid[:, shift_amount:] ensures we keep the 2D structure
    shifted_part = input_grid[:, shift_amount:] # Shape will be (1, 12 - shift_amount)

    # Create the 2D padding array with the correct shape (1, shift_amount)
    # Use the same data type as the input grid for consistency
    padding = np.full((1, shift_amount), pad_value, dtype=input_grid.dtype) # Shape (1, shift_amount)

    # Concatenate the shifted part and the padding along the column axis (axis=1)
    output_sequence_2d = np.concatenate((shifted_part, padding), axis=1) # Shape (1, 12)

    # The result is a 2D array (1x12). We need to format the single row.
    # Flatten() converts it to 1D, or access the first row directly output_sequence_2d[0]
    output_sequence_1d = output_sequence_2d.flatten()

    # Format the resulting 1D NumPy array into a space-separated string
    output_str = format_output(output_sequence_1d)

    # Return the formatted string
    return output_str