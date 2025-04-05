import math
import numpy as np # Although not strictly needed for this logic, it's often available

"""
1. Identify the index of the number `2` in the input sequence.
2. Find the index of the rightmost non-zero number located *before* the index of `2`. Let this number be `left_fill_value`. If such a number exists, replace all zeros between its index (exclusive) and the index of `2` (exclusive) with `left_fill_value`.
3. Find the index of the leftmost non-zero number located *after* the index of `2`. Let this number be `right_fill_value`. If such a number exists, replace all zeros between the index of `2` (exclusive) and its index (exclusive) with `right_fill_value`.
4. Return the modified sequence.
"""

def find_index(sequence, value):
    """Helper function to find the first index of a value in a sequence."""
    try:
        return sequence.index(value)
    except ValueError:
        return -1 # Indicate not found

def transform(input_str):
    """
    Applies a fill operation on a sequence of integers based on the position of the number 2.
    Zeros between the number 2 and the nearest non-zero numbers on either side are filled
    with those respective non-zero numbers.
    """
    # Convert input string to a list of integers
    input_list = [int(x) for x in input_str.split()]
    
    # Initialize output_list as a copy of the input to modify it
    output_list = list(input_list)
    n = len(output_list)

    # 1. Identify the index of the number 2
    marker_index = find_index(output_list, 2)

    # If 2 is not found (shouldn't happen based on examples, but good practice)
    if marker_index == -1:
        return " ".join(map(str, output_list)) # Return original if 2 is missing

    # 2. Find the rightmost non-zero number *before* 2 and fill leftwards
    left_fill_value = 0
    left_fill_index = -1
    for i in range(marker_index - 1, -1, -1):
        if output_list[i] != 0:
            left_fill_value = output_list[i]
            left_fill_index = i
            break # Found the closest non-zero to the left

    # If a left fill value was found, fill the zeros between it and the marker
    if left_fill_index != -1:
        for i in range(left_fill_index + 1, marker_index):
            if output_list[i] == 0:
                output_list[i] = left_fill_value

    # 3. Find the leftmost non-zero number *after* 2 and fill rightwards
    right_fill_value = 0
    right_fill_index = -1
    for i in range(marker_index + 1, n):
        if output_list[i] != 0:
            right_fill_value = output_list[i]
            right_fill_index = i
            break # Found the closest non-zero to the right

    # If a right fill value was found, fill the zeros between the marker and it
    if right_fill_index != -1:
        for i in range(marker_index + 1, right_fill_index):
             if output_list[i] == 0:
                output_list[i] = right_fill_value

    # 4. Return the modified sequence as a space-separated string
    return " ".join(map(str, output_list))
