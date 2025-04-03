import numpy as np
from typing import List, Tuple, Optional

"""
Transformation Rule:
Move a contiguous block of non-background (0), non-pivot (9) colored pixels 
relative to a fixed pivot pixel (9) within a 1D array.

1.  Identify the single pivot pixel (maroon '9') and its index (`pivot_index`).
2.  Identify the contiguous block of pixels with the same color, which is neither 
    white ('0') nor maroon ('9'). Record its color, data (`object_data`), 
    start index (`object_start_index`), and end index (`object_end_index`).
3.  Calculate the number of background pixels ('0') strictly between the end of the 
    object block and the pivot pixel in the input array (`gap_size`). Based on the 
    examples, the object appears before the pivot.
4.  Initialize an output array of the same size as the input, filled with the 
    background color (white '0').
5.  Place the pivot pixel ('9') at `pivot_index` in the output array.
6.  Calculate the starting index for the object block in the output array: 
    `output_object_start_index = pivot_index + gap_size + 1`.
7.  Place the `object_data` into the output array, starting at 
    `output_object_start_index`.
"""

def find_pivot(input_list: List[int]) -> Optional[int]:
    """Finds the index of the pivot element (9)."""
    try:
        return input_list.index(9)
    except ValueError:
        return None # Pivot not found

def find_object_block(input_list: List[int]) -> Optional[Tuple[List[int], int, int]]:
    """
    Finds the first contiguous block of non-0, non-9 pixels.
    Returns the block data, start index, and end index.
    """
    object_data = []
    object_start_index = -1
    object_end_index = -1
    in_block = False
    block_color = -1

    for i, val in enumerate(input_list):
        is_object_pixel = (val != 0 and val != 9)

        if is_object_pixel:
            if not in_block:  # Start of a new block
                object_start_index = i
                block_color = val
                in_block = True
                object_data.append(val)
            elif val == block_color: # Continue existing block
                object_data.append(val)
            else: # Encountered a different color - treat as end of block
                  # (or could be an error based on stricter interpretation)
                  # For now, assume first block is the target
                  object_end_index = i - 1
                  break
        elif in_block: # End of the block (found 0 or 9)
            object_end_index = i - 1
            break # Found the block, stop searching

    # Handle case where block goes to the end of the list
    if in_block and object_end_index == -1:
        object_end_index = len(input_list) - 1

    if object_start_index != -1:
        return object_data, object_start_index, object_end_index
    else:
        return None # No object block found

def calculate_gap_size(input_list: List[int], object_end_index: int, pivot_index: int) -> int:
    """Calculates the number of 0s between the object and the pivot."""
    # Assuming object is before pivot based on examples
    if object_end_index >= pivot_index -1:
         return 0 # No space between or overlapping/adjacent

    gap_slice = input_list[object_end_index + 1 : pivot_index]
    gap_size = gap_slice.count(0)
    return gap_size

def transform(input_grid: List[int]) -> List[int]:
    """
    Applies the transformation rule to move the object block relative to the pivot.
    Assumes input_grid is a 1D list based on example format.
    """
    input_list = input_grid # Use clearer name
    list_len = len(input_list)

    # Initialize output_list with background color (0)
    output_list = [0] * list_len

    # Find the pivot pixel (9)
    pivot_index = find_pivot(input_list)
    if pivot_index is None:
        # Handle error: Pivot not found (though examples guarantee it)
        # For now, return the empty grid or raise error
        print("Error: Pivot (9) not found.")
        return output_list # Or potentially raise ValueError

    # Place the pivot in the output list
    output_list[pivot_index] = 9

    # Find the object block (contiguous, non-0, non-9)
    object_info = find_object_block(input_list)
    if object_info is None:
        # Handle error: Object block not found
        print("Error: Object block not found.")
        # Return grid with only pivot placed, as per examples? Yes.
        return output_list 

    object_data, object_start_index, object_end_index = object_info

    # Calculate the gap size (number of 0s) between object end and pivot start
    # Based on examples, the object is always before the pivot.
    gap_size = calculate_gap_size(input_list, object_end_index, pivot_index)

    # Calculate the new starting position for the object block in the output
    output_object_start_index = pivot_index + gap_size + 1

    # Calculate the end position for slicing
    output_object_end_index = output_object_start_index + len(object_data)

    # Place the object block into the output list, ensuring bounds are respected
    if output_object_start_index < list_len:
        # Determine how many elements can actually fit
        elements_to_place = min(len(object_data), list_len - output_object_start_index)
        
        for i in range(elements_to_place):
             output_list[output_object_start_index + i] = object_data[i]

    # Return the transformed list
    return output_list
