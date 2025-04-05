import math
import numpy as np

"""
1. Identify the contiguous block of identical non-zero digits in the input sequence. 
   Determine its value, starting position (index), and length.
2. Calculate the new starting position for this block by subtracting 4 from its original starting position.
3. Create a new sequence of the same length as the input, initially filled entirely with zeros.
4. Place the identified non-zero block (using its value and length) into the new sequence 
   starting at the calculated new position.
5. The resulting sequence is the output.
"""

def _parse_input(input_str):
    """Converts the space-separated string of digits into a list of integers."""
    return [int(d) for d in input_str.split()]

def _find_non_zero_block(int_list):
    """Finds the start index, value, and length of the first contiguous non-zero block."""
    start_index = -1
    value = 0
    length = 0
    in_block = False
    for i, digit in enumerate(int_list):
        if digit != 0 and not in_block:
            # Start of a new block
            start_index = i
            value = digit
            length = 1
            in_block = True
        elif digit == value and in_block:
            # Continuing the block
            length += 1
        elif digit != value and in_block:
            # End of the block
            break # Assuming only one block per input based on examples
    if start_index == -1: # Handle case with all zeros (though not in examples)
        return None
    return {'value': value, 'start': start_index, 'length': length}

def _format_output(int_list):
    """Converts a list of integers back into a space-separated string."""
    return " ".join(map(str, int_list))

def transform(input_str):
    """
    Shifts the first contiguous block of identical non-zero digits 4 positions 
    to the left within a sequence of digits, filling other positions with zero.
    """
    # Convert input string to list of integers
    input_list = _parse_input(input_str)
    n = len(input_list)

    # Initialize output_list with zeros
    output_list = [0] * n

    # Find the non-zero block in the input
    block_info = _find_non_zero_block(input_list)

    # If a block is found, place it in the output list at the shifted position
    if block_info:
        value = block_info['value']
        original_start = block_info['start']
        length = block_info['length']
        
        # Calculate the new starting position (shift left by 4)
        new_start = original_start - 4
        
        # Place the block into the output list
        # Ensure indices stay within bounds (though not strictly necessary 
        # if input guarantees valid shifts)
        for i in range(length):
            idx = new_start + i
            # Check if the index is valid before assignment
            if 0 <= idx < n: 
                 output_list[idx] = value

    # Convert the output list back to a space-separated string
    output_str = _format_output(output_list)

    return output_str