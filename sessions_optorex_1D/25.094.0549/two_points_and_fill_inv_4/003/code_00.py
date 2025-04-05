"""
Identifies contiguous blocks of identical non-zero numbers in the input sequence.
If a block's length is greater than 2, it 'hollows out' the block in the output sequence 
by setting all elements except the first and last to zero. Blocks of length 1 or 2, 
and sequences of zeros, remain unchanged.
"""

from itertools import groupby
import math # math is available but not used in this solution
# No other specific science libraries needed for this logic.

def transform(input_sequence: list[int]) -> list[int]:
    """
    Applies the hollowing transformation to blocks of non-zero numbers longer than 2.

    Args:
        input_sequence: A list of integers representing the input sequence.

    Returns:
        A new list of integers representing the transformed sequence.
    """
    
    # Initialize output_sequence as a mutable copy of the input sequence.
    # This ensures that elements not explicitly modified retain their original values.
    output_sequence = list(input_sequence) 
    
    current_index = 0
    # Iterate through the input sequence, grouping consecutive identical elements.
    # `groupby` yields the value and an iterator for the group of consecutive identical elements.
    for value, group in groupby(input_sequence):
        
        # Determine the length of the current contiguous block.
        # We need to consume the iterator `group` to find its length.
        block_list = list(group) 
        block_length = len(block_list)
        
        # Calculate the start and end indices (inclusive) of the current block in the sequence.
        start_index = current_index
        end_index = current_index + block_length - 1
        
        # Check the condition for hollowing: 
        # 1. The block must consist of non-zero numbers.
        # 2. The block's length must be strictly greater than 2.
        if value != 0 and block_length > 2:
            # Apply the 'hollow_out_block' action.
            # Iterate through the *interior* indices of the block in the output sequence.
            # The range starts from the element *after* the first (start_index + 1)
            # and goes up to, but does not include, the last element (end_index).
            for i in range(start_index + 1, end_index):
                # Set the interior elements to 0.
                output_sequence[i] = 0
                
        # Move the current_index to the position immediately after the current block
        # to prepare for processing the next block.
        current_index += block_length

    # Return the modified output sequence.
    return output_sequence