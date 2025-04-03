"""
Identifies a single contiguous block of identical non-zero integers within a 12-element input sequence provided as a space-separated string. Shifts this block 2 positions to the right within a new sequence of 12 zeros. Elements shifted beyond the right boundary (index 11) are discarded. Returns the transformed sequence as a space-separated string. If the input contains no non-zero block, returns a string of 12 zeros separated by spaces.
"""

import numpy as np # numpy is available, though not strictly required here
import re # re could be used but iteration is clear

def find_block(grid_list):
    """
    Finds the first contiguous block of identical non-zero numbers in a list.

    Args:
        grid_list: A list of integers.

    Returns:
        A tuple (value, start_index, end_index) representing the block's value
        and its start/end indices. Returns (None, -1, -1) if no non-zero
        block is found.
    """
    start_index = -1
    end_index = -1
    value = None
    n = len(grid_list)

    for i, val in enumerate(grid_list):
        if val != 0:
            # Found the start of a potential block
            if start_index == -1:
                start_index = i
                value = val
            # Check if the current value matches the block's value
            elif val != value:
                # Found a different non-zero value, ending the first block.
                end_index = i - 1
                break
        elif start_index != -1:
            # Found a zero after the block started, mark the end
            end_index = i - 1
            break

    # Handle block extending to the very end of the grid
    if start_index != -1 and end_index == -1:
         # If we found a start but no end yet, determine the true end of the *first* block.
         current_end = start_index
         for k in range(start_index + 1, n):
              if grid_list[k] == value:
                  current_end = k
              else:
                  break # Stop at the first element that doesn't match
         end_index = current_end

    # Check if a block was actually found
    if value is None:
        return None, -1, -1

    # Ensure end_index is at least start_index (for single element blocks)
    if end_index < start_index:
         end_index = start_index

    return value, start_index, end_index


def transform(input_str):
    """
    Applies the block shifting transformation to the input string.

    Args:
        input_str: A string containing 12 space-separated integers.

    Returns:
        A string containing 12 space-separated integers representing the transformed sequence.
    """
    # 1. Parse the input string into a list of integers
    try:
        input_list = [int(x) for x in input_str.split()]
        grid_size = 12 # Expecting fixed size based on examples
        if len(input_list) != grid_size:
             # Handle potential malformed input gracefully, though examples are consistent
             print(f"Warning: Input '{input_str}' does not contain exactly {grid_size} elements.")
             # Fallback: return empty or zero string based on expected format
             return " ".join(['0'] * grid_size)
    except ValueError:
        # Handle non-integer input
        print(f"Warning: Input '{input_str}' contains non-integer values.")
        return " ".join(['0'] * grid_size)


    # 2. Initialize the output grid with zeros
    output_list = [0] * grid_size

    # 3. Find the non-zero block in the input list
    value, start_idx, end_idx = find_block(input_list)

    # 4. If no block is found, return the grid of zeros as a string
    if value is None:
        return " ".join(map(str, output_list))

    # 5. Define the shift amount
    shift_distance = 2

    # 6. Calculate the new position for the block
    new_start_idx = start_idx + shift_distance
    new_end_idx = end_idx + shift_distance

    # 7. Place the block in the output list at the new position, handling boundaries
    # Iterate through the *original* indices of the block to determine which elements land within bounds
    for i in range(start_idx, end_idx + 1):
        target_idx = i + shift_distance
        # Check if the target index is within the grid bounds
        if 0 <= target_idx < grid_size:
            # Place the block's value at the valid target index
            output_list[target_idx] = value

    # 8. Convert the output list back to a space-separated string
    output_str = " ".join(map(str, output_list))

    # 9. Return the resulting string
    return output_str