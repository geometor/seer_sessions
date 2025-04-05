```python
import math
import numpy as np # Using numpy for easier array manipulation if needed, though list slicing is sufficient here

"""
Identifies the contiguous block of non-zero numbers in the input list, 
shifts this block 3 positions to the right, and places it into an 
output list of the same size, padded with zeros elsewhere.
"""

def _find_non_zero_indices(data_list):
    """
    Finds the start and end indices of the first contiguous block of non-zero numbers.
    Returns (None, None) if no non-zero numbers are found.
    """
    first_nz_index = None
    last_nz_index = None
    for i, val in enumerate(data_list):
        if val != 0:
            if first_nz_index is None:
                first_nz_index = i
            last_nz_index = i
    return first_nz_index, last_nz_index

def transform(input_list):
    """
    Transforms the input list by shifting the block of non-zero numbers 3 positions to the right.

    Args:
        input_list: A list of integers.

    Returns:
        A new list of integers with the non-zero block shifted.
    """
    # Determine the length of the list
    list_length = len(input_list)

    # Initialize output_list with zeros, same length as input
    output_list = [0] * list_length

    # 1. Find the start and end indices of the non-zero block
    first_nz_index, last_nz_index = _find_non_zero_indices(input_list)

    # 2. Check if a non-zero block was found
    if first_nz_index is not None:
        # 3. Extract the non-zero block
        non_zero_block = input_list[first_nz_index : last_nz_index + 1]

        # 4. Calculate the new starting position for the block
        new_start_index = first_nz_index + 3
        
        # 5. Place the block into the output list at the new position
        # Ensure we don't write past the end of the output list
        block_len = len(non_zero_block)
        end_placement_index = new_start_index + block_len
        
        # Calculate how much of the block fits
        elements_to_place = block_len
        if end_placement_index > list_length:
             elements_to_place = list_length - new_start_index
             
        if elements_to_place > 0 and new_start_index < list_length:
             output_list[new_start_index : new_start_index + elements_to_place] = non_zero_block[:elements_to_place]


    # 6. Return the constructed output list
    return output_list

```