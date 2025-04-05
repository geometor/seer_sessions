import math
import numpy as np # Although not strictly needed for this specific logic, 
                   # it's often useful for grid manipulations. Keeping it for potential future use.

"""
Identifies a contiguous block of a non-zero digit within a sequence of digits (represented as a space-separated string) and shifts this block three positions to the left. The sequence length is maintained, and positions outside the shifted block are filled with zeros.
"""

def find_non_zero_block(int_list):
    """
    Finds the first contiguous block of identical non-zero digits.

    Args:
        int_list: A list of integers.

    Returns:
        A tuple (value, start_index, end_index) if a block is found,
        otherwise None. end_index is exclusive (like Python slicing).
    """
    start_index = -1
    block_value = -1
    for i, val in enumerate(int_list):
        if val != 0:
            start_index = i
            block_value = val
            break # Found the start of the block

    if start_index == -1:
        return None # No non-zero elements found

    end_index = start_index
    while end_index < len(int_list) and int_list[end_index] == block_value:
        end_index += 1

    return block_value, start_index, end_index


def transform(input_str):
    """
    Transforms the input sequence by shifting the non-zero block left by 3 positions.

    Args:
        input_str: A string representing a space-separated sequence of digits.

    Returns:
        A string representing the transformed space-separated sequence.
    """
    # 1. Parse Input: Convert the input string into a list of integers.
    try:
        input_list = [int(x) for x in input_str.split()]
    except ValueError:
        # Handle cases where input might not be purely digits/spaces
        print(f"Warning: Could not parse input string: {input_str}")
        return input_str # Or raise an error, or return default

    n = len(input_list)
    if n == 0:
        return ""

    # 2. Find Non-Zero Block
    block_info = find_non_zero_block(input_list)

    # Initialize output grid (list) with zeros
    output_list = [0] * n

    if block_info:
        block_value, start_index, end_index = block_info
        block_length = end_index - start_index

        # 3. Calculate New Start position for the block
        # Shift left by 3, ensuring it doesn't go below index 0
        new_start_index = max(0, start_index - 3)

        # 4. Construct Output: Place the block at the new position
        # Iterate through the length of the original block
        for i in range(block_length):
            # Calculate the target index in the output list
            target_index = new_start_index + i
            
            # Check if the target index is within the bounds of the output list
            if 0 <= target_index < n:
                # Place the block's value at the target index
                output_list[target_index] = block_value
                
    # 5. Format Output: Join the elements of the output list back into a space-separated string.
    output_str = " ".join(map(str, output_list))
    
    return output_str
