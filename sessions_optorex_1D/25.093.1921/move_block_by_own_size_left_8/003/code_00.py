"""
Transforms an input sequence of digits by identifying the single contiguous block 
of a non-zero digit and shifting this block leftward by a distance equal to 
its own length. The resulting sequence maintains the original length, with 
positions outside the shifted block filled with zeros.
"""

import typing

def find_non_zero_block(sequence: typing.List[int]) -> typing.Tuple[typing.Optional[int], int, int]:
    """
    Finds the first contiguous block of a non-zero digit in the sequence.

    Args:
        sequence: The input list of integers.

    Returns:
        A tuple containing:
        - The non-zero digit found (or None if no non-zero digit exists).
        - The starting index of the block (-1 if not found).
        - The length of the block (0 if not found).
    """
    digit = None
    start_index = -1
    length = 0
    in_block = False

    for i, value in enumerate(sequence):
        if value != 0:
            # Found the start of the block
            if not in_block:
                digit = value
                start_index = i
                length = 1
                in_block = True
            # Continue counting within the block (must be the same digit)
            elif value == digit:
                length += 1
            # Found a different non-zero digit - this violates the assumption
            # of a single block type, but based on task description, we assume
            # the first block ends here or is the only one.
            else: 
                break 
        elif in_block:
            # Found a zero after the block started, so the block ended
            break
            
    # If no non-zero digit was ever found
    if not in_block:
        return None, -1, 0
        
    return digit, start_index, length

def transform(input_grid: typing.List[int]) -> typing.List[int]:
    # 1. Determine the length of the input sequence.
    sequence_length = len(input_grid)
    
    # 2. Create a new output sequence of the same length, initializing all its elements to zero.
    output_grid = [0] * sequence_length

    # 3. Scan the input sequence to locate the contiguous block of non-zero digits.
    #    Record the non-zero digit itself, the starting index, and the length.
    digit, start_index_input, block_length = find_non_zero_block(input_grid)

    # Handle case where no non-zero block is found (input is all zeros)
    if digit is None:
        return output_grid 

    # 4. Calculate the target starting index for the block in the output sequence.
    #    Target Start = Original Start - Block Length
    target_start_index_output = start_index_input - block_length

    # 5. Iterate and place the block's digits into the output sequence.
    for i in range(block_length):
        # Calculate the index in the output sequence for the current digit of the block
        output_index = target_start_index_output + i
        
        # Ensure the index is within the valid range of the output grid
        if 0 <= output_index < sequence_length:
            # Place the non-zero digit at the calculated index
            output_grid[output_index] = digit
        # else: # If the index is out of bounds, that part of the block is clipped (though examples don't show this)
        #    pass 

    # 6. Return the completed output sequence.
    return output_grid