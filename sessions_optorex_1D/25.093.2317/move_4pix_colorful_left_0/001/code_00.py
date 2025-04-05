import numpy as np
import math

"""
Transforms an input sequence of digits by identifying the contiguous block 
between the first and last non-zero digits, and shifting this block 4 positions 
to the left within a sequence of the same length, padding with zeros.
"""

def find_first_nonzero_index(data):
    """Finds the index of the first non-zero element in a list."""
    for i, x in enumerate(data):
        if x != 0:
            return i
    return None  # Return None if no non-zero element is found

def find_last_nonzero_index(data):
    """Finds the index of the last non-zero element in a list."""
    for i in range(len(data) - 1, -1, -1):
        if data[i] != 0:
            return i
    return None # Return None if no non-zero element is found

def transform(input_str):
    """
    Applies the transformation rule to the input string.

    Args:
        input_str: A string of space-separated single digits.

    Returns:
        A string of space-separated single digits representing the transformed sequence.
    """
    # Parse the input string into a list of integers
    input_sequence = [int(d) for d in input_str.split()]
    n = len(input_sequence)

    # Initialize the output sequence with zeros
    output_sequence = [0] * n

    # Find the indices of the first and last non-zero digits
    first_nz_idx = find_first_nonzero_index(input_sequence)
    last_nz_idx = find_last_nonzero_index(input_sequence)

    # If no non-zero digits are found, return the sequence of zeros
    if first_nz_idx is None:
        return " ".join(map(str, output_sequence))

    # Extract the contiguous block including zeros between the first and last non-zero digits
    digit_block = input_sequence[first_nz_idx : last_nz_idx + 1]

    # Calculate the target starting index for the block in the output
    # Shift is 4 positions to the left
    output_start_idx = first_nz_idx - 4

    # Ensure the start index is not negative (although examples suggest it won't be)
    # It seems the minimum first_nz_idx allowing a valid shift is 4 (e.g., train_1)
    # If first_nz_idx were less than 4, the logic might need adjustment,
    # but based on examples, we assume first_nz_idx >= 4 if non-zeros exist.
    # Or more accurately, the calculation output_start_idx >= 0 holds for the examples.
    output_start_idx = max(0, output_start_idx) # safeguard, though likely not needed for provided examples

    # Calculate the end index for placing the block in the output
    output_end_idx = output_start_idx + len(digit_block)

    # Place the extracted block into the output sequence
    # Ensure the block fits within the output sequence bounds
    if output_start_idx < n and output_end_idx <= n:
        output_sequence[output_start_idx:output_end_idx] = digit_block
    # Handle cases where the block might theoretically go out of bounds (if input rules change)
    elif output_start_idx < n:
         # Place as much of the block as fits
         length_to_copy = n - output_start_idx
         output_sequence[output_start_idx:] = digit_block[:length_to_copy]


    # Format the output sequence back into a space-separated string
    output_str = " ".join(map(str, output_sequence))

    return output_str