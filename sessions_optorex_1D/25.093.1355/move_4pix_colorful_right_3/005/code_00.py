import math
# numpy is not strictly needed but available if complex array ops were required
# import numpy as np 
import re # Not needed for this specific transformation

"""
Transforms an input sequence of 12 integers by shifting its elements 4 positions 
to the right. Elements shifted off the right end are discarded. The 4 leftmost 
positions (indices 0, 1, 2, 3) are filled with zeros. Handles potential input 
wrapping where the sequence might be nested within another list.
"""

def _unwrap_input(raw_input_data, expected_length):
    """
    Checks for nested list input and returns the effective sequence.
    
    Args:
        raw_input_data: The input received by the transform function.
        expected_length: The expected length of the inner sequence.

    Returns:
        The effective sequence (list) or raises ValueError if input is invalid.
    """
    # Check if it's a list containing a single list of the correct length
    if (isinstance(raw_input_data, list) and
            len(raw_input_data) == 1 and
            isinstance(raw_input_data[0], list) and
            len(raw_input_data[0]) == expected_length):
        # Unwrap the inner list
        return raw_input_data[0]
    # Check if it's already a flat list of the correct length
    elif isinstance(raw_input_data, list) and len(raw_input_data) == expected_length:
        # Input is already in the expected format
        return raw_input_data
    # Otherwise, the input format is unexpected/invalid
    else:
        # Consider raising a more specific error or returning None depending on desired behavior
        raise ValueError(f"Invalid input format. Expected a list of {expected_length} integers "
                         f"or a list containing a single such list. Got: {type(raw_input_data)}")


def transform(input_sequence_raw):
    """
    Applies a right shift of 4 positions to the input sequence.

    Args:
        input_sequence_raw: A sequence (list or potentially list[list]) 
                            containing 12 integers.

    Returns:
        A list containing the transformed 12 integers.
    """
    # --- Constants ---
    SEQUENCE_LENGTH = 12
    SHIFT_AMOUNT = 4

    # --- Input Processing ---
    # Unwrap the input if necessary to get the actual sequence
    try:
        input_list = _unwrap_input(input_sequence_raw, SEQUENCE_LENGTH)
    except ValueError as e:
        # Handle error appropriately, e.g., log it or re-raise
        print(f"Error processing input: {e}")
        # Returning an empty list or raising might be alternatives
        return [0] * SEQUENCE_LENGTH # Return default state on error

    # --- Initialization ---
    # Initialize the output list with zeros. This handles the left padding.
    output_list = [0] * SEQUENCE_LENGTH

    # --- Transformation (Right Shift) ---
    # Iterate through the input elements that will fit into the shifted output.
    # Only elements from input index 0 to SEQUENCE_LENGTH - SHIFT_AMOUNT - 1 (i.e., 0 to 7)
    # will be placed into the output list. Elements from index 8 onwards are truncated.
    for i in range(SEQUENCE_LENGTH - SHIFT_AMOUNT):
        # Calculate the target index in the output list
        target_index = i + SHIFT_AMOUNT
        
        # Copy the input element to the calculated shifted position in the output
        output_list[target_index] = input_list[i]

    # --- Return Result ---
    return output_list