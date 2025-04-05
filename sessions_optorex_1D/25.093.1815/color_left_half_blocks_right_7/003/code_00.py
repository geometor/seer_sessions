"""
Transforms a sequence of integers (0s and 2s) based on contiguous blocks of the value 2.
For each contiguous block of k twos, the first floor(k / 2) twos are changed to 8,
while the remaining twos stay as 2. Zeros remain unchanged.
The input is expected to be a sequence (like a list or NumPy array) of integers.
The output will be a list of integers.
"""

import math # // operator handles floor division, but keeping import for clarity if needed
import numpy as np # To handle potential NumPy array input

def transform(input_sequence):
    """
    Applies the transformation rule to the input sequence.

    Args:
        input_sequence: A list or NumPy array containing integers (0s and 2s).

    Returns:
        A list of integers representing the transformed sequence.
    """
    
    # Ensure input is a list for easy element modification.
    # Create a copy to avoid modifying the original input if it's a list.
    if isinstance(input_sequence, np.ndarray):
        output_list = input_sequence.tolist()
    elif isinstance(input_sequence, list):
        output_list = list(input_sequence) # Create a copy
    else:
        # Attempt to convert other sequence types, raise error if not possible
        try:
            output_list = list(input_sequence)
        except TypeError:
            raise TypeError("Input must be a sequence type (e.g., list, tuple, numpy array)")

    n = len(output_list)
    i = 0 # Current index in the sequence

    # Iterate through the sequence to find and process blocks of 2s
    while i < n:
        # Check if the current element is the start of a block of 2s
        if output_list[i] == 2:
            # Record the starting index of the block
            start_index = i
            
            # Find the end of the block and count its length
            block_length = 0
            while i < n and output_list[i] == 2:
                block_length += 1
                i += 1 # Move index forward
            # 'i' now points to the element *after* the block, or is equal to n if block ends the sequence
            
            # Calculate how many 2s in this block should be changed to 8s
            num_to_change = block_length // 2  # Integer division provides floor(block_length / 2)

            # Modify the elements in the output_list for this block
            for j in range(start_index, start_index + num_to_change):
                output_list[j] = 8
            
            # The outer loop's index 'i' is already positioned correctly
            # to continue searching *after* the processed block, so no further adjustment needed here.
            
        else:
            # If the current element is not 2 (must be 0), just move to the next element
            i += 1

    # Return the transformed list
    return output_list