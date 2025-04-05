import math
import numpy as np
# Add other necessary imports here if needed, though basic list operations suffice

"""
Transforms an input sequence of 12 integers by finding the single contiguous block 
of identical non-zero integers and shifting this block 4 positions to the left. 
Positions in the output sequence are filled with zeros initially, and then 
populated by the shifted block values where applicable within the sequence boundaries.
Elements shifted beyond the left boundary (index < 0) are discarded.
"""

def find_nonzero_block(sequence):
    """
    Finds the first contiguous block of identical non-zero integers in the sequence.

    Args:
        sequence: A list of integers.

    Returns:
        A tuple containing:
        - value (int): The non-zero value of the block (or 0 if no block found).
        - start_index (int): The starting index of the block (-1 if no block found).
        - length (int): The length of the block (0 if no block found).
    """
    start_index = -1
    value = 0
    length = 0
    n = len(sequence)

    # Iterate through the sequence to find the start of the block
    for i in range(n):
        # Find the start of a potential block
        if sequence[i] != 0 and start_index == -1:
            start_index = i
            value = sequence[i]
            length = 1 # Start counting length
        # If we've found the start, check if the block continues
        elif start_index != -1:
            if sequence[i] == value:
                length += 1 # Increment length
            else:
                # Block ends here (either different non-zero or zero)
                break # Exit loop once the contiguous block ends

    # If no block was found (start_index remained -1), return defaults
    if start_index == -1:
        return 0, -1, 0
        
    return value, start_index, length

def transform(input_grid):
    # Determine the length of the sequence (assumed to be 12 from examples)
    sequence_length = len(input_grid) 

    # 1. Initialize Output: Create a new sequence of the same length, filled with zeros.
    output_grid = [0] * sequence_length

    # 2. Identify Block: Find the non-zero block details in the input sequence.
    block_value, start_index, block_length = find_nonzero_block(input_grid)

    # Proceed only if a valid block was found (start_index is not -1)
    if start_index != -1:
        # 3. Calculate Target Position: Determine the target starting index for the block
        # by shifting the original start index 4 positions to the left.
        new_start_index = start_index - 4

        # 4. Place Block: Populate the output grid with the shifted block's values.
        # Iterate through each position relative to the start of the block (0 to length-1).
        for i in range(block_length):
            # Calculate the target index in the output sequence for this element of the block.
            target_idx = new_start_index + i

            # Check if the calculated target index is within the valid bounds of the output grid (0 to sequence_length-1).
            if 0 <= target_idx < sequence_length:
                # If the index is valid, place the block's value at that position in the output grid.
                output_grid[target_idx] = block_value
            # If target_idx is outside the bounds (e.g., < 0), that part of the block is effectively discarded.

    # 5. Finalize: Return the constructed output grid.
    return output_grid