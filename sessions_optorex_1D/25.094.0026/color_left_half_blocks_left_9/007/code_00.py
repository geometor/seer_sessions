"""
Transforms an input sequence of integers based on the length of contiguous blocks of the number 2.
The transformation rules are applied to a copy of the input sequence:
- If a contiguous block of 2s has length k=1, no change occurs.
- If a contiguous block of 2s has length k=2 or k=3, the last 2 in the block is changed to 8.
- If a contiguous block of 2s has length k>=4, the last two 2s in the block are changed to 8.
- Elements with value 0 remain unchanged.
"""

import math 
# No specific complex libraries needed for this logic (like numpy)

# Helper function (optional, but can clarify finding block length)
def find_block_length(sequence, start_index):
    """Finds the length of a contiguous block of 2s starting at start_index."""
    length = 0
    n = len(sequence)
    j = start_index
    while j < n and sequence[j] == 2:
        length += 1
        j += 1
    return length

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
        # Check if the current element is the start of a block of 2s
        if input_sequence[i] == 2:
            # Found the start of a potential block
            block_start_index = i
            
            # Find the length of the contiguous block of '2's
            # Use a counter approach directly within the main loop
            block_length = 0
            j = i 
            while j < n and input_sequence[j] == 2:
                block_length += 1
                j += 1
            # Block ends just before index j. Its length is block_length.
            
            # Apply transformation rules based on the determined block_length
            # These rules modify the output_sequence directly
            if block_length == 2 or block_length == 3:
                # Change the last '2' (index block_start + block_length - 1) to 8
                # Boundary checks are implicitly handled because j stopped within bounds or at n
                last_index = block_start_index + block_length - 1
                output_sequence[last_index] = 8
            elif block_length >= 4:
                # Change the last two '2's 
                # Index of last element
                last_index = block_start_index + block_length - 1 
                # Index of second-to-last element
                second_last_index = block_start_index + block_length - 2 
                
                output_sequence[last_index] = 8
                output_sequence[second_last_index] = 8
            # No action needed for block_length == 1

            # Advance the main loop index past the processed block
            # j is already at the index immediately following the block
            i = j 
        else:
            # Current element is 0 (or not 2), just move to the next element
            i += 1

    # Return the modified sequence
    return output_sequence