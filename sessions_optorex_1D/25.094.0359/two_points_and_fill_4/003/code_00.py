import numpy as np
import math

"""
Transforms an input grid (represented as a list containing a single list of integers, or a 1xN NumPy array) 
by filling the zeros within the single row/list between the first and last non-zero digits found in that row/list.
The fill value propagates from left to right, starting with the value of the first non-zero digit,
and updating whenever a new non-zero digit is encountered in the input row/list within that range.
Zeros outside the range defined by the first and last non-zero digits remain unchanged.
The output grid retains the same structure (list of list or NumPy array) as the input.
"""

def find_first_nonzero_index(sequence):
    """Finds the index of the first non-zero element in a 1D sequence."""
    for i, val in enumerate(sequence):
        if val != 0:
            return i
    return -1 # Return -1 if no non-zero element is found

def find_last_nonzero_index(sequence):
    """Finds the index of the last non-zero element in a 1D sequence."""
    # Iterate backwards to find the last one efficiently
    for i in range(len(sequence) - 1, -1, -1):
        if sequence[i] != 0:
            return i
    return -1 # Return -1 if no non-zero element is found

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list containing a single list of integers, or a 1xN NumPy array.

    Returns:
        The transformed grid in the same format as the input.
    """

    # Determine input type and extract the inner sequence
    is_numpy = isinstance(input_grid, np.ndarray)
    if is_numpy:
        if input_grid.ndim != 2 or input_grid.shape[0] != 1:
             # Handle cases that don't match the expected 1xN shape if necessary
             # For now, assume valid input as per examples
            pass
        inner_sequence = input_grid[0, :].tolist() # Work with a list copy
    elif isinstance(input_grid, list) and len(input_grid) == 1 and isinstance(input_grid[0], list):
        inner_sequence = input_grid[0]
    else:
        # Handle unexpected input format if necessary
        raise TypeError("Input must be a 1xN NumPy array or a list containing a single list.")

    # Find the index of the first non-zero digit in the inner sequence
    first_idx = find_first_nonzero_index(inner_sequence)

    # Find the index of the last non-zero digit in the inner sequence
    last_idx = find_last_nonzero_index(inner_sequence)

    # If no non-zero digits are found, or only one is found (so no range to fill),
    # return the original input grid structure unchanged.
    if first_idx == -1 or first_idx == last_idx:
        # Ensure a copy is returned if the input might be mutable (like a list)
        # and the caller expects a new object. NumPy arrays might be less of an issue here.
        if is_numpy:
            return np.copy(input_grid)
        else:
            # Create a deep copy for lists to avoid modifying the original input structure
            return [list(inner_sequence)]


    # Create the output sequence as a copy of the inner sequence to modify
    output_sequence = list(inner_sequence)

    # Initialize fill_value with the value of the digit at first_idx
    fill_value = inner_sequence[first_idx]

    # Iterate through the indices from first_idx up to last_idx (inclusive)
    for i in range(first_idx, last_idx + 1):
        # Check the digit at index i in the *original* inner sequence.
        # If this digit is non-zero, update fill_value
        if inner_sequence[i] != 0:
            fill_value = inner_sequence[i]

        # Check the digit at index i in the *output* sequence.
        # If this digit is 0, change its value to the current fill_value
        # Note: We check output_sequence[i] because a non-zero value from the input
        # should not be overwritten, even if it's within the fill range.
        # The condition could equivalently be `if inner_sequence[i] == 0:`,
        # because non-zeros are handled by the previous `if`.
        if output_sequence[i] == 0:
            output_sequence[i] = fill_value

    # Reconstruct the output grid in the original format
    if is_numpy:
        # Convert the modified list back to a 1xN NumPy array
        output_grid = np.array([output_sequence], dtype=input_grid.dtype) # Preserve original dtype
    else:
        # Wrap the modified list in another list
        output_grid = [output_sequence]

    # Return the reconstructed output grid
    return output_grid