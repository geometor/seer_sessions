import math
import numpy as np
import re # Using re for potentially more complex string parsing if needed later, though split() is sufficient now.

"""
Transformation Rule:
1. Find the digit '2' in the input sequence.
2. Identify contiguous sequences of '0's immediately adjacent to the '2' on either side.
3. Look for the first non-'0', non-'2' digit encountered when moving away from the '2' past these '0' sequences.
4. If such a digit ('source_digit') is found and the sequence between it and the '2' consists only of '0's, replace those '0's with the 'source_digit'.
5. Perform this check and potential fill operation independently for the left and right sides of the '2'.
6. If '2' is not present, or if the conditions for filling are not met on either side, the sequence remains unchanged in that region.
"""

def _parse_input(input_str: str) -> list[int]:
    """Parses the space-separated string into a list of integers."""
    return [int(x) for x in input_str.split()]

def _format_output(output_list: list[int]) -> str:
    """Formats the list of integers back into a space-separated string."""
    return " ".join(map(str, output_list))

def transform(input_str: str) -> str:
    """
    Applies the transformation rule to the input string sequence.
    Finds '2', identifies adjacent '0' sequences, finds the nearest
    non-zero/non-2 source digits, and fills the '0's towards the '2'
    if the intermediate region is all '0's.
    """
    input_list = _parse_input(input_str)
    output_list = list(input_list) # Create a modifiable copy
    n = len(output_list)

    # Find the index of the boundary marker '2'
    idx_2 = -1
    try:
        idx_2 = input_list.index(2)
    except ValueError:
        # '2' is not in the list, return the original sequence
        return input_str

    # --- Fill Left ---
    idx_left = -1
    source_left = -1
    # Scan leftwards from idx_2 - 1 to find the first non-0, non-2 digit
    for i in range(idx_2 - 1, -1, -1):
        if output_list[i] != 0 and output_list[i] != 2:
            idx_left = i
            source_left = output_list[i]
            break # Found the first source digit

    # If a potential source digit was found on the left
    if idx_left != -1:
        # Check if all elements between idx_left and idx_2 are '0'
        all_zeros_between = True
        for i in range(idx_left + 1, idx_2):
            if output_list[i] != 0:
                all_zeros_between = False
                break
        
        # If the condition is met, fill the zeros
        if all_zeros_between:
            for i in range(idx_left + 1, idx_2):
                output_list[i] = source_left

    # --- Fill Right ---
    idx_right = -1
    source_right = -1
    # Scan rightwards from idx_2 + 1 to find the first non-0, non-2 digit
    for i in range(idx_2 + 1, n):
        if output_list[i] != 0 and output_list[i] != 2:
            idx_right = i
            source_right = output_list[i]
            break # Found the first source digit

    # If a potential source digit was found on the right
    if idx_right != -1:
        # Check if all elements between idx_2 and idx_right are '0'
        all_zeros_between = True
        for i in range(idx_2 + 1, idx_right):
            if output_list[i] != 0:
                all_zeros_between = False
                break

        # If the condition is met, fill the zeros
        if all_zeros_between:
            for i in range(idx_2 + 1, idx_right):
                output_list[i] = source_right

    # Format the modified list back into a string
    return _format_output(output_list)
