"""
Transforms an input sequence (represented as a string of space-separated digits) 
by identifying a single, contiguous block of identical non-zero digits and shifting 
this block 3 positions to the left. The output sequence has the same length as the 
input, with the background filled with zeros. Digits shifted beyond the start of 
the sequence are truncated. The output is also formatted as a string of space-separated 
digits.
"""

import math # math and science libraries are available, though not needed here
import numpy as np # numpy is available, though not strictly needed for this logic

def find_non_zero_block(sequence):
    """
    Finds the contiguous block of identical non-zero digits in a sequence.

    Args:
        sequence: A list or 1D numpy array of integers.

    Returns:
        A tuple containing:
        - start_index: The starting index of the block (or None if not found).
        - length: The length of the block (or 0 if not found).
        - value: The digit value of the block (or None if not found).
    """
    start_index = None
    length = 0
    value = None
    in_block = False

    # Iterate through the sequence with index and digit
    for i, digit in enumerate(sequence):
        # If not currently in a block and the digit is non-zero, start a new block
        if not in_block and digit != 0:
            start_index = i
            value = digit
            length = 1
            in_block = True
        # If currently in a block
        elif in_block:
            # If the digit matches the block's value, extend the block length
            if digit == value:
                length += 1
            # If the digit is different (or zero), the block ends
            else:
                # Since we assume only one block based on examples, stop searching
                break 
    
    # Handle the case where no non-zero block was found
    if not in_block: 
        return None, 0, None
        
    # Return the properties of the found block
    return start_index, length, value

def transform(input_str):
    """
    Applies the left-shift transformation to the input sequence string.

    Args:
        input_str: A string of space-separated integers representing the input sequence.

    Returns:
        A string of space-separated integers representing the transformed sequence.
    """
    # 1. Parse the input string into a list of integers.
    input_sequence = [int(d) for d in input_str.split()]
    n = len(input_sequence)

    # 2. Initialize the output sequence as a list of zeros with the same length.
    output_sequence = [0] * n

    # 3. Find the contiguous block of non-zero digits in the input.
    start_index, length, value = find_non_zero_block(input_sequence)

    # 4. If no block is found (e.g., input is all zeros), return the zero sequence formatted as a string.
    if start_index is None:
        return " ".join(map(str, output_sequence))

    # 5. Calculate the target starting index for the block in the output sequence (shift left by 3).
    new_start_index = start_index - 3

    # 6. Place the non-zero block into the output sequence at the new position.
    # Iterate 'length' times, once for each digit in the block.
    for i in range(length):
        # Calculate the specific index in the output sequence for the current digit.
        current_output_index = new_start_index + i
        
        # Check if this calculated index is valid (within the bounds 0 to n-1).
        if 0 <= current_output_index < n:
            # If the index is valid, place the non-zero digit value at that position.
             output_sequence[current_output_index] = value
        # If the index is out of bounds (e.g., negative), the digit is effectively truncated.

    # 7. Convert the elements of the output list back into strings.
    output_strings = [str(digit) for digit in output_sequence]

    # 8. Join the string elements with single spaces to form the final output string.
    output_str = " ".join(output_strings)

    # 9. Return the resulting output string.
    return output_str