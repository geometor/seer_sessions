import re
from typing import List, Optional, Tuple

"""
Identifies the sub-sequence spanning from the first non-zero element to the last non-zero element 
in the input sequence. This sub-sequence is then shifted 3 positions to the right within a new 
sequence of the same length, initially filled with zeros. If the input sequence contains only 
zeros, the output sequence also contains only zeros.
"""

def find_non_zero_span(numbers: List[int]) -> Optional[Tuple[int, int]]:
    """
    Finds the indices of the first and last non-zero elements in the list.

    Args:
        numbers: A list of integers.

    Returns:
        A tuple containing the start and end indices (inclusive) of the span
        containing all non-zero numbers, or None if all numbers are zero.
    """
    start_index = -1
    end_index = -1
    for i, num in enumerate(numbers):
        if num != 0:
            if start_index == -1:
                start_index = i
            end_index = i
    
    if start_index == -1:
        return None
    else:
        return start_index, end_index

def transform(input_str: str) -> str:
    """
    Transforms the input sequence string based on the described rule.

    Args:
        input_str: A string representing a sequence of space-separated integers.

    Returns:
        A string representing the transformed sequence of space-separated integers.
    """
    # Parse input string into a list of integers
    input_list = [int(x) for x in input_str.split()]
    n = len(input_list)

    # Initialize output list with zeros
    output_list = [0] * n

    # Find the span of non-zero numbers in the input
    span = find_non_zero_span(input_list)

    # If a non-zero span exists
    if span:
        start_index, end_index = span
        
        # Extract the block of numbers within the span
        non_zero_block = input_list[start_index : end_index + 1]
        
        # Calculate the new starting position (shifted right by 3)
        new_start_index = start_index + 3
        
        # Place the block into the output list at the new position
        # Ensure we don't write past the end of the output list
        block_len = len(non_zero_block)
        if new_start_index < n:
            # Determine how many elements of the block can fit
            elements_to_copy = min(block_len, n - new_start_index)
            for i in range(elements_to_copy):
                 output_list[new_start_index + i] = non_zero_block[i]

    # Format the output list back into a space-separated string
    return " ".join(map(str, output_list))
