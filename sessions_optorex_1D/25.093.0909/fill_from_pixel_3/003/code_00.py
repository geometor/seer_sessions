import numpy as np

"""
Transforms a 1D sequence of integers based on its first and last non-zero elements.

1.  Find the first non-zero integer (`first_val`) and its position (`first_idx`).
2.  Find the last non-zero integer (`last_val`) and its position (`last_idx`).
3.  If no non-zero integers are found (the sequence is all zeros), return a copy of the input.
4.  Otherwise, calculate the sum `S = first_val + last_val`.
5.  If `S` is greater than or equal to 14:
    a. Change all elements in a copy of the sequence from position `last_idx + 1` to the end to the value `last_val` (Right Expansion).
6.  Else (if `S` is less than 14):
    a. Change all elements in a copy of the sequence from the beginning (position 0) up to (but not including) position `first_idx` to the value `first_val` (Left Expansion).
7.  Return the modified sequence.
"""

def find_first_last_non_zero(sequence):
    """
    Finds the value and index of the first and last non-zero elements in a NumPy array.

    Args:
        sequence: A 1D NumPy array of integers.

    Returns:
        A tuple: (first_val, first_idx, last_val, last_idx).
        Returns (None, -1, None, -1) if no non-zero elements are found.
    """
    # Find indices of all non-zero elements
    non_zero_indices = np.nonzero(sequence)[0]

    # Check if any non-zero elements exist
    if non_zero_indices.size == 0:
        return None, -1, None, -1

    # Get the first and last indices
    first_idx = non_zero_indices[0]
    last_idx = non_zero_indices[-1]

    # Get the values at these indices
    first_val = sequence[first_idx]
    last_val = sequence[last_idx]

    return first_val, first_idx, last_val, last_idx


def transform(input_sequence: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input sequence (NumPy array).

    Args:
        input_sequence: A 1D NumPy array of integers.

    Returns:
        A new 1D NumPy array representing the transformed sequence.
    """
    # Ensure input is a numpy array for consistency
    if not isinstance(input_sequence, np.ndarray):
        input_sequence = np.array(input_sequence) # convert list to numpy

    # Find the first and last non-zero elements and their indices
    first_val, first_idx, last_val, last_idx = find_first_last_non_zero(input_sequence)

    # Handle the case where the sequence is all zeros
    if first_val is None:
        return input_sequence.copy() # Return a copy

    # Calculate the sum
    s = first_val + last_val

    # Create a copy of the input sequence to modify
    output_sequence = input_sequence.copy()

    # Apply the transformation based on the sum
    if s >= 14:
        # Right Expansion: Change trailing zeros
        # Use slicing to modify elements from last_idx + 1 to the end
        if last_idx + 1 < len(output_sequence): # Check if there are trailing elements
            output_sequence[last_idx + 1:] = last_val
    else:
        # Left Expansion: Change leading zeros
        # Use slicing to modify elements from the beginning up to first_idx
        if first_idx > 0: # Check if there are leading elements
             output_sequence[:first_idx] = first_val

    return output_sequence