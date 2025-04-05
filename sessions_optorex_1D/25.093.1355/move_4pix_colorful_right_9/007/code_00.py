"""
Transforms an input sequence (numpy array) of 12 integers by shifting the first 8 elements 4 positions to the right. The first 4 positions of the output sequence are filled with zeros, and elements shifted beyond the 12th position (index 11) are effectively truncated as they are not copied.
"""

import numpy as np

def transform(input_sequence: np.ndarray) -> np.ndarray:
    """
    Applies a right shift transformation to the input sequence.

    Args:
        input_sequence: A NumPy array containing 12 integers.

    Returns:
        A NumPy array containing the transformed 12 integers.
    """
    # Define fixed parameters based on observation
    sequence_length = 12
    shift_amount = 4

    # 1. Create a new output sequence initialized with zeros (padding)
    # The size is determined by the fixed sequence length.
    output_sequence = np.zeros(sequence_length, dtype=int)

    # 2. Determine the slice of the input sequence to copy.
    # We copy elements from the beginning up to the point where they would be shifted off the end.
    # Source indices: 0 to (sequence_length - shift_amount - 1) => 0 to 7
    source_slice = input_sequence[0 : sequence_length - shift_amount]

    # 3. Determine the slice in the output sequence where the copied elements will be placed.
    # Destination indices: shift_amount to (sequence_length - 1) => 4 to 11
    destination_slice_start = shift_amount
    destination_slice_end = sequence_length

    # 4. Perform the slice assignment: copy the selected input elements to the shifted position in the output.
    output_sequence[destination_slice_start : destination_slice_end] = source_slice

    # 5. Return the completed output sequence
    return output_sequence