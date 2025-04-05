import numpy as np
from typing import List, Tuple

"""
Transforms a sequence of integers by replacing contiguous blocks of '5's.

The transformation rule is as follows:
1.  Identify the first two numbers in the input sequence as `key1` and `key2`.
2.  Find all contiguous blocks (sequences) of the number 5 in the input sequence.
3.  If at least one block of 5s exists, replace the elements corresponding to the *first* block with `key1`.
4.  If at least two blocks of 5s exist, replace the elements corresponding to the *second* block with `key2`.
5.  All other numbers in the sequence remain unchanged in their positions.
"""

def find_contiguous_blocks(sequence: List[int], target_value: int) -> List[Tuple[int, int]]:
    """
    Finds contiguous blocks of a target value in a sequence.

    Args:
        sequence: The list of integers to search within.
        target_value: The integer value to find blocks of.

    Returns:
        A list of tuples, where each tuple contains (start_index, length)
        of a contiguous block. Returns an empty list if no blocks are found.
    """
    blocks = []
    n = len(sequence)
    i = 0
    while i < n:
        if sequence[i] == target_value:
            start_index = i
            length = 0
            # Continue while the value matches the target and we're within bounds
            while i < n and sequence[i] == target_value:
                length += 1
                i += 1
            blocks.append((start_index, length))
        else:
            # Move to the next element if no block starts here
            i += 1
    return blocks

def transform(input_sequence: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input numpy array sequence.

    Args:
        input_sequence: A 1D numpy array containing integers.

    Returns:
        A 1D numpy array containing the transformed integers.
    """
    # Ensure the input is treated as a standard Python list for block finding logic
    # This also handles potential type issues if the array dtype isn't standard int
    input_list = input_sequence.tolist()

    # Initialize the output sequence as a copy of the input
    # We'll modify this copy
    output_sequence = np.copy(input_sequence)

    # Check if the input sequence is long enough to have keys
    if len(input_list) < 2:
        # If sequence is too short, return the original sequence
        # Or handle as an error/edge case depending on requirements
        # Based on examples, sequences are always long enough.
        return output_sequence 

    # Identify key1 and key2 from the input sequence
    key1 = input_list[0]
    key2 = input_list[1]

    # Define the target digit to search for
    target_digit = 5

    # Find all contiguous blocks of the target_digit (5) in the list representation
    target_blocks = find_contiguous_blocks(input_list, target_digit)

    # Replace the elements of the first block with key1, if it exists
    if len(target_blocks) >= 1:
        start_index, length = target_blocks[0]
        # Use numpy slicing for efficient replacement in the output array
        end_index = start_index + length
        # Ensure slicing doesn't go out of bounds (though it shouldn't if logic is correct)
        if end_index <= len(output_sequence):
             output_sequence[start_index:end_index] = key1

    # Replace the elements of the second block with key2, if it exists
    if len(target_blocks) >= 2:
        start_index, length = target_blocks[1]
        # Use numpy slicing for efficient replacement
        end_index = start_index + length
        if end_index <= len(output_sequence):
            output_sequence[start_index:end_index] = key2

    # Return the modified numpy array
    return output_sequence