import numpy as np
import collections

"""
Transforms a sequence of 12 integers based on the following rules:
1.  Accept the input sequence (a list or array of 12 integers).
2.  Identify a 'pivot' element (always the digit '2'). Record its index.
3.  Identify a contiguous block of identical digits (the 'payload') that are not '0' or '2'. Record its value, length, and starting index.
4.  Create a new output sequence of the same length (12), initialized with '0's.
5.  Place the 'pivot' element ('2') in the new sequence at the same index it occupied in the input sequence.
6.  Determine the target start index for placing the payload block in the output sequence:
    - If the payload was originally to the left of the pivot (payload_start_index < pivot_index), the target start index is pivot_index - payload_length.
    - If the payload was originally to the right of the pivot (payload_start_index > pivot_index), the target start index is pivot_index + 1.
7.  Place the 'payload' block (repeating payload_value for payload_length times) into the output sequence starting at the calculated target start index.
8.  Return the completed output sequence.
"""

def find_pivot_index(grid):
    """Finds the index of the pivot element '2'."""
    # Convert to list if it's a numpy array for easier index finding
    grid_list = list(grid)
    try:
        return grid_list.index(2)
    except ValueError:
        # This case is assumed not to happen based on the problem description
        return -1

def find_payload_block(grid):
    """
    Finds the payload block (value, length, start_index).
    Returns a tuple (payload_value, payload_length, payload_start_index)
    or (None, 0, -1) if no payload is found.
    """
    payload_value = None
    payload_length = 0
    payload_start_index = -1

    i = 0
    while i < len(grid):
        # Look for a digit that is not 0 and not 2
        if grid[i] != 0 and grid[i] != 2:
            # Found the start of a potential payload block
            payload_value = grid[i]
            payload_start_index = i
            payload_length = 1
            # Count the length of the contiguous block of the same digit
            j = i + 1
            while j < len(grid) and grid[j] == payload_value:
                payload_length += 1
                j += 1
            # Found the complete block, no need to search further
            break
        i += 1

    if payload_value is None:
         # This case is assumed not to happen based on the problem description
         return (None, 0, -1)

    return payload_value, payload_length, payload_start_index

def transform(input_grid):
    """
    Applies the transformation rule to the input grid (list or NumPy array).
    """
    # Ensure input is treated as a list for easier manipulation
    # (handles both list and numpy array inputs)
    input_list = list(input_grid)
    n = len(input_list)

    # initialize output_grid with zeros
    output_grid = [0] * n

    # Find the pivot element '2' and its index
    pivot_index = find_pivot_index(input_list)
    if pivot_index == -1:
        # Return original grid or handle error if pivot not found
        return input_list # Or np.array(input_list) if output must be array

    # Find the payload block's properties
    payload_value, payload_length, payload_start_index = find_payload_block(input_list)
    if payload_value is None:
        # Return original grid or handle error if payload not found
        return input_list # Or np.array(input_list)

    # Place the pivot element '2' in the output grid
    output_grid[pivot_index] = 2

    # Determine the target start index for the payload block
    target_start_index = -1
    if payload_start_index < pivot_index:
        # Payload was originally to the left, place it immediately left of the pivot
        target_start_index = pivot_index - payload_length
    else: # payload_start_index > pivot_index (cannot be equal as payload != 2)
        # Payload was originally to the right, place it immediately right of the pivot
        target_start_index = pivot_index + 1

    # Place the payload block in the output grid
    for i in range(payload_length):
        placement_index = target_start_index + i
        # Basic bounds check, though based on rules it should fit
        if 0 <= placement_index < n:
            output_grid[placement_index] = payload_value
        else:
            # Handle potential out-of-bounds placement if necessary,
            # though problem constraints suggest this won't happen.
            print(f"Warning: Calculated placement index {placement_index} out of bounds.")


    # Return the transformed grid as a NumPy array, as is common in ARC tasks
    return np.array(output_grid)
