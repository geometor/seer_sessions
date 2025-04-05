"""
Transforms an input sequence of integers based on the length of contiguous blocks of the number 2.
The transformation rules are applied to a copy of the input sequence:
- If a contiguous block of 2s has length k=2, the second 2 in the block is changed to 8.
- If a contiguous block of 2s has length k=3, the third 2 in the block is changed to 8.
- If a contiguous block of 2s has length k>=4, the last two 2s in the block are changed to 8.
- Elements with value 0 and 2s not modified by the above rules remain unchanged.
"""

import math
# No numpy needed for this logic

def transform(input_sequence):
    """
    Applies block-based transformation rules to the input sequence.

    Args:
        input_sequence: A list of integers (0s and 2s).

    Returns:
        A list of integers (0s, 2s, and 8s) representing the transformed sequence.
    """
    # Initialize output_sequence as a mutable copy of the input
    output_sequence = list(input_sequence) 
    n = len(input_sequence)
    
    # Handle empty input
    if n == 0:
        return output_sequence

    i = 0
    # Iterate through the sequence to find blocks of '2's
    while i < n:
        if input_sequence[i] == 2:
            # Found the start of a potential block
            block_start = i
            block_length = 0
            # Count the length of the contiguous block of '2's
            while i < n and input_sequence[i] == 2:
                block_length += 1
                i += 1
            # Block ended (or sequence ended). i is now at the index AFTER the block.
            
            # Apply transformation rules based on the determined block_length
            if block_length == 2:
                # Change the second '2' (index block_start + 1) to 8
                # Boundary check (block_start + 1 < n) is implicitly handled by loop structure
                output_sequence[block_start + 1] = 8
            elif block_length == 3:
                # Change the third '2' (index block_start + 2) to 8
                output_sequence[block_start + 2] = 8
            elif block_length >= 4:
                # Change the last two '2's (indices block_start + block_length - 2 and -1) to 8
                if block_start + block_length - 1 < n: # Ensure index is valid
                    output_sequence[block_start + block_length - 1] = 8
                if block_start + block_length - 2 < n: # Ensure index is valid
                   output_sequence[block_start + block_length - 2] = 8
            # Continue the outer loop from index i (which is already past the processed block)
        else:
            # Current element is 0, just move to the next element
            i += 1

    # Return the modified sequence
    return output_sequence