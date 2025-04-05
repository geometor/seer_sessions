"""
Transforms a 1D NumPy array of integers by preserving only the first and last
elements of contiguous blocks of identical non-zero numbers longer than 
two elements. The middle elements of such blocks (between the first and last) 
are changed to zero. Original zeros and blocks of length 1 or 2 remain unchanged.
"""

import numpy as np
import copy

def find_blocks(sequence):
    """
    Identifies contiguous blocks of identical non-zero numbers in a sequence.

    Args:
        sequence: A 1D NumPy array or list of integers.

    Returns:
        A list of tuples, where each tuple represents a block:
        (value, start_index, end_index).
    """
    blocks = []
    # Use len() which works for both lists and NumPy arrays
    if len(sequence) == 0:
        return blocks

    start_index = None
    current_value = None

    for i, value in enumerate(sequence):
        # Comparison with 0 works fine for NumPy integer types
        if value != 0: 
            if start_index is None:
                # Start of a potential new block
                start_index = i
                current_value = value
            # Comparison between NumPy integer types works fine
            elif value != current_value: 
                # End of the previous block, start of a new one
                blocks.append((current_value, start_index, i - 1))
                start_index = i
                current_value = value
        elif start_index is not None:
            # End of the current block due to encountering a zero
            blocks.append((current_value, start_index, i - 1))
            start_index = None
            current_value = None

    # Handle the case where a block extends to the end of the sequence
    if start_index is not None:
        blocks.append((current_value, start_index, len(sequence) - 1))

    return blocks

def transform(input_sequence):
    """
    Applies the block transformation rule to the input sequence.

    Args:
        input_sequence: A 1D NumPy array of integers.

    Returns:
        A 1D NumPy array with the transformation applied.
    """
    # 1. Accept the input sequence (already done by argument passing).
    # Ensure it's a NumPy array for consistency, although copy.deepcopy often handles lists too.
    # Using np.copy is generally preferred for NumPy arrays.
    if not isinstance(input_sequence, np.ndarray):
         # Convert if necessary, though framework likely provides numpy arrays
         input_sequence = np.array(input_sequence) 

    # 2. Create a deep copy of the input NumPy array for the output.
    output_sequence = np.copy(input_sequence) # Use np.copy for NumPy arrays

    # 3. Check if the input sequence is empty (handled in find_blocks, but good practice).
    if len(input_sequence) == 0:
        return output_sequence

    # 4-6. Identify contiguous blocks of identical non-zero numbers.
    blocks = find_blocks(input_sequence)

    # 7. Iterate through the identified blocks.
    for value, start_index, end_index in blocks:
        # a. Calculate the block's length.
        block_length = end_index - start_index + 1
        
        # b. If length is greater than 2:
        if block_length > 2:
            # i. Iterate through the indices strictly between the start and end index.
            # Note: range(start + 1, end) correctly selects the middle elements.
            for i in range(start_index + 1, end_index):
                # ii. Set the element in the *output* sequence at index i to 0.
                # Direct assignment works fine with NumPy arrays.
                output_sequence[i] = 0
                
    # 8. Return the modified output sequence.
    return output_sequence