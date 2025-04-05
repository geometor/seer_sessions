import math
import collections

"""
Transforms a sequence of single-digit integers based on contiguous blocks of identical non-zero digits.

1.  Initialize the output sequence as a direct copy of the input sequence.
2.  Iterate through the input sequence from left to right to identify contiguous blocks (runs) of identical non-zero digits.
3.  For each identified block where the length is greater than 2:
    a.  Iterate through the indices strictly *between* the start and end indices of the block.
    b.  Set the value in the output sequence at these intermediate indices to 0.
4.  Digits that are initially '0' remain '0'. Blocks of length 1 or 2 remain unchanged.
5.  Return the modified output sequence.
"""

def transform(input_sequence):
    """
    Applies the transformation rule to the input sequence.

    Args:
        input_sequence: A list of integers representing the input sequence.

    Returns:
        A list of integers representing the transformed output sequence.
    """
    n = len(input_sequence)
    # Initialize output_sequence as a copy of the input
    output_sequence = list(input_sequence)

    i = 0
    while i < n:
        # Skip over zeros
        if input_sequence[i] == 0:
            i += 1
            continue

        # Found a non-zero digit, potential start of a block
        start_index = i
        block_value = input_sequence[i]
        end_index = i

        # Find the end of the contiguous block of the same non-zero digit
        j = i + 1
        while j < n and input_sequence[j] == block_value:
            end_index = j
            j += 1

        # Calculate the length of the identified block
        block_length = end_index - start_index + 1

        # If the block length is greater than 2, zero out the middle elements
        if block_length > 2:
            # Iterate through the indices strictly between start_index and end_index
            for k in range(start_index + 1, end_index):
                output_sequence[k] = 0

        # Move the main iterator past the processed block
        i = end_index + 1

    return output_sequence
