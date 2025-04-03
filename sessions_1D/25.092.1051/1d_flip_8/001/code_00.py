import numpy as np
from typing import List

"""
Identify the contiguous sequence of non-white (non-zero) pixels in the input row.
Extract this sequence.
Modify the extracted sequence by moving its first element (pixel) to the end of the sequence.
Create the output row by placing the modified sequence back into the same positions it occupied in the input row, keeping all white (zero) pixels in their original locations.
"""

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms a 1D grid by finding the first contiguous block of non-zero pixels
    and performing a left cyclic shift (moving the first element to the end)
    within that block, leaving zero pixels untouched.

    Args:
        input_grid: A list containing a single list (representing the 1D row) of integers.

    Returns:
        A list containing a single list representing the transformed 1D row.
    """
    # Since the input is described as 1D, work with the first row.
    input_row = input_grid[0]
    output_row = list(input_row) # Create a mutable copy

    # Find the start and end indices of the contiguous non-zero sequence
    start_index = -1
    end_index = -1
    in_sequence = False

    for i, pixel in enumerate(input_row):
        if pixel != 0 and not in_sequence:
            start_index = i
            in_sequence = True
        elif pixel == 0 and in_sequence:
            end_index = i - 1
            break # Found the end of the sequence

    # If the sequence runs to the end of the row
    if in_sequence and end_index == -1:
        end_index = len(input_row) - 1

    # Check if a sequence was found and its length is greater than 1
    if start_index != -1 and end_index >= start_index and (end_index - start_index + 1) > 1:
        # Extract the sequence
        sequence = output_row[start_index : end_index + 1]

        # Perform the left cyclic shift
        first_element = sequence.pop(0)
        sequence.append(first_element)

        # Place the transformed sequence back into the output row
        output_row[start_index : end_index + 1] = sequence

    # Return the result in the expected list-of-lists format
    return [output_row]
