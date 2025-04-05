import math
import numpy as np
# Add other imports as needed, e.g., from collections import Counter

"""
Transforms a sequence of integers by swapping elements at the first detected boundary between a zero and a non-zero digit.

The transformation rule depends on the type of the first boundary encountered when scanning from left to right:
1. If a non-zero element is followed by a zero element (at indices i and i+1), swap these two elements.
2. If a zero element is followed by a non-zero element (at indices i and i+1), find the start index 'k' of the contiguous block of zeros ending at index 'i'. Swap the element at index 'k' (the first zero of the block) with the non-zero element at index 'i+1'.
The transformation stops after the first boundary is processed.
"""

def find_first_zero_block_start(sequence, end_index):
    """Helper function to find the start index of a block of zeros ending at end_index."""
    start_index = end_index
    while start_index >= 0 and sequence[start_index] == 0:
        start_index -= 1
    # The loop stops when sequence[start_index] is non-zero or start_index is -1.
    # The actual start of the zero block is the next index.
    return start_index + 1

def transform(input_sequence):
    """
    Applies the boundary swap transformation to the input sequence.

    Args:
        input_sequence: A list of integers.

    Returns:
        A new list of integers representing the transformed sequence.
    """
    # Initialize output_sequence as a copy of the input
    output_sequence = list(input_sequence)
    n = len(output_sequence)

    # Iterate through the sequence to find the first boundary
    for i in range(n - 1):
        current_is_zero = (output_sequence[i] == 0)
        next_is_zero = (output_sequence[i+1] == 0)

        # Check if a boundary exists (one is zero, the other is not)
        if current_is_zero != next_is_zero:
            # Boundary found at index i

            # Case 1: Non-zero followed by Zero (Type 1 Boundary)
            if not current_is_zero and next_is_zero:
                # Swap the non-zero at i with the zero at i+1
                output_sequence[i], output_sequence[i+1] = output_sequence[i+1], output_sequence[i]
                # Break after processing the first boundary
                break

            # Case 2: Zero followed by Non-zero (Type 2 Boundary)
            elif current_is_zero and not next_is_zero:
                # Find the start index 'k' of the zero block ending at 'i'
                k = find_first_zero_block_start(output_sequence, i)
                # Swap the first zero of the block (at k) with the non-zero at i+1
                output_sequence[k], output_sequence[i+1] = output_sequence[i+1], output_sequence[k]
                # Break after processing the first boundary
                break

    # Return the modified sequence
    return output_sequence