"""
Transforms an input sequence of digits by identifying the single contiguous block 
of a non-zero digit and shifting this block leftward by a distance equal to 
its own length. The resulting sequence maintains the original length, with 
positions outside the shifted block filled with zeros.
"""

import typing
# It's good practice to import numpy if the execution environment might use it,
# even if the core logic aims for standard Python lists. This acknowledges
# the potential input type.
import numpy as np 

# Helper Function to find the non-zero block details
def find_non_zero_block(sequence: typing.Union[typing.List[int], np.ndarray]) -> typing.Tuple[typing.Optional[int], int, int]:
    """
    Finds the first contiguous block of a non-zero digit in the sequence.

    Args:
        sequence: The input list or NumPy array of integers.

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

    # Iterate through the sequence element by element
    for i, value in enumerate(sequence):
        # Check if the current element is non-zero
        if value != 0:
            # If we haven't started a block yet, this is the beginning
            if not in_block:
                digit = int(value) # Store the digit value
                start_index = i    # Store the starting index
                length = 1         # Initialize length
                in_block = True    # Mark that we are inside a block
            # If we are already in a block, check if it's the same digit
            elif value == digit:
                length += 1        # Increment length if it's the same digit
            # If we encounter a *different* non-zero digit, the first block ends.
            # Based on the problem description (single block), we stop processing the block here.
            else: 
                break 
        # If we encounter a zero *after* having been in a block
        elif in_block:
            # The contiguous block has ended
            break
            
    # If no non-zero digit was ever found
    if not in_block:
        return None, -1, 0 # Return indicator values for "not found"
        
    # Return the found digit, its start index, and its length
    return digit, start_index, length

def transform(input_grid: typing.Union[typing.List[int], np.ndarray]) -> typing.List[int]:
    """
    Applies the transformation rule to the input grid.
    
    Args:
        input_grid: A list or NumPy array representing the input sequence.
        
    Returns:
        A list representing the transformed sequence.
    """
    # 1. Determine the length of the input sequence.
    # Using len() works for both Python lists and NumPy arrays.
    sequence_length = len(input_grid)
    
    # 2. Create an output sequence (as a Python list) of the same length, 
    #    initializing all its elements to zero.
    output_grid = [0] * sequence_length

    # 3. Scan the input sequence to locate the contiguous block of non-zero digits.
    #    Record the non-zero digit itself, the starting index, and the length.
    digit, start_index_input, block_length = find_non_zero_block(input_grid)

    # 4. If no non-zero block is found (input is all zeros), return the zero-filled output sequence.
    if digit is None:
        return output_grid 

    # 5. Calculate the target starting index for the block in the output sequence.
    #    Target Start = Original Start - Block Length (Shift Amount)
    target_start_index_output = start_index_input - block_length

    # 6. Iterate and place the block's digits into the output sequence.
    #    Iterate 'block_length' times to place each digit of the block.
    for i in range(block_length):
        # Calculate the specific index in the output sequence for the current digit of the block
        output_index = target_start_index_output + i
        
        # Check if the calculated index is within the valid bounds (0 to length-1) of the output sequence.
        # This prevents errors if the shift moves the block partially or fully off the left edge.
        if 0 <= output_index < sequence_length:
            # Place the non-zero digit at the calculated index in the output sequence.
            output_grid[output_index] = digit
        # else: 
            # If the index is out of bounds, that part of the block is clipped.
            # The examples provided don't show this happening, but the check adds robustness.
            # No action needed here as the position is outside the grid.

    # 7. Return the completed output sequence (as a Python list).
    return output_grid