import math
from itertools import groupby

"""
Identifies contiguous blocks of identical non-zero numbers in the input sequence.
If a block's length is greater than 2, it 'hollows out' the block in the output sequence 
by setting all elements except the first and last to zero. Blocks of length 1 or 2, 
and sequences of zeros, remain unchanged.
"""

def transform(input_sequence: list[int]) -> list[int]:
    """
    Applies the hollowing transformation to blocks of non-zero numbers longer than 2.

    Args:
        input_sequence: A list of integers.

    Returns:
        A new list of integers representing the transformed sequence.
    """
    # Initialize output_sequence as a copy of the input
    output_sequence = list(input_sequence)
    
    current_index = 0
    # Iterate through the input sequence, grouping consecutive identical elements
    for value, group in groupby(input_sequence):
        # Convert the group iterator to a list to easily get its length
        block = list(group)
        block_length = len(block)
        
        # Calculate the start and end indices of the current block
        start_index = current_index
        end_index = current_index + block_length - 1
        
        # Check if the block consists of non-zero numbers and has a length greater than 2
        if value != 0 and block_length > 2:
            # Modify the output sequence: set interior elements of the block to 0
            for i in range(start_index + 1, end_index):
                output_sequence[i] = 0
                
        # Update the current index to the start of the next block
        current_index += block_length

    # Return the modified sequence
    return output_sequence
