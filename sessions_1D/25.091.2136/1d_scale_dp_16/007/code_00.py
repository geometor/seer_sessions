"""
Transforms an input 1D sequence (list) of integers based on the rule:
1. Find the first occurrence of the marker value 6 (magenta).
2. Find the last non-zero value (fill color) that occurs before this marker. Record its index (block_end_index).
3. Identify the sequence segment (gap) strictly between block_end_index and the marker index.
4. Change all zero values (white pixels) within this gap to the identified fill color.
5. Leave all other values unchanged.
"""

import copy
# numpy is not strictly necessary here as standard list operations suffice
# import numpy as np 

def find_first_occurrence(sequence, value):
    """Finds the index of the first occurrence of a value in a list."""
    try:
        return sequence.index(value)
    except ValueError:
        return -1 # Value not found

def find_last_non_zero_before_index(sequence, limit_index):
    """
    Finds the index and value of the last non-zero element before a given index.
    Searches backwards from limit_index - 1.
    """
    for i in range(limit_index - 1, -1, -1):
        if sequence[i] != 0:
            return i, sequence[i] # Return index and value (fill_color)
    return -1, -1 # No non-zero element found

def transform(input_grid):
    """
    Applies the transformation rule to the input grid (assumed to be a 1D list).

    Args:
        input_grid: A list of integers representing the input sequence.

    Returns:
        A new list of integers representing the transformed sequence.
        Returns a copy of the input if the transformation cannot be applied
        (e.g., no marker or no fill block found).
    """
    # Ensure input is a list (basic type checking)
    if not isinstance(input_grid, list):
        # Using deepcopy just in case the input structure is more complex than expected
        # though for 1D lists of ints, list() or slicing [:] would work.
        # In ARC context, inputs should be lists or numpy arrays. If numpy, convert.
        # For this specific task structure, assuming list input is safe based on examples.
        # Consider adding numpy handling if needed for broader ARC compatibility.
        return copy.deepcopy(input_grid) 

    # 1. Initialize an output sequence as a copy of the input sequence.
    output_grid = list(input_grid)

    # 2. Scan the input sequence from left to right to find the index of the first magenta pixel (value 6).
    marker_index = find_first_occurrence(output_grid, 6)

    # If no marker is found, return the unmodified output sequence.
    if marker_index == -1:
        return output_grid

    # 3. Scan backwards from marker_index - 1 to find the first non-zero pixel.
    # 4. Identify its index (fill_source_index) and value (fill_color).
    fill_source_index, fill_color = find_last_non_zero_before_index(output_grid, marker_index)

    # If no non-white pixel is found before the marker, return the unmodified output sequence.
    if fill_source_index == -1:
        return output_grid

    # 5. Iterate through the indices k starting from fill_source_index + 1 up to (but not including) marker_index.
    # This defines the 'gap'.
    gap_start_index = fill_source_index + 1
    gap_end_index = marker_index # range() is exclusive of the end index

    for i in range(gap_start_index, gap_end_index):
        # 6. Check if the value at the current index in the gap is white (0).
        if output_grid[i] == 0:
            # 7. If it is white, update its value to fill_color.
            output_grid[i] = fill_color
        # Pixels in the gap that are not 0 remain unchanged.

    # 8. Return the modified output sequence.
    return output_grid