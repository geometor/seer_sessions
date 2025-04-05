import numpy as np
from typing import List, Tuple, Optional

"""
Transformation Rule Natural Language Description:

1.  Receive the input, expecting a NumPy array of 12 integers.
2.  Convert the input NumPy array into a Python list (`input_list`).
3.  Create an `output_list` of 12 zeros.
4.  Find the index (`pivot_index`) of the integer `2` within the `input_list`. If `2` is not found, return the `input_list` as is (error condition).
5.  Place the integer `2` at the `pivot_index` in the `output_list`.
6.  Scan the `input_list` to locate the first contiguous block of non-zero integers, excluding the element at `pivot_index`. Record its starting index (`block_start`), ending index (`block_end`), and the sequence of values (`block_values`).
7.  If no such data block is found, return the `output_list` (containing only the `2` and zeros).
8.  Determine the relative position of the block to the `pivot_index`:
    *   If `block_end < pivot_index`, the block is "Left". Calculate `gap = pivot_index - block_end - 1`.
    *   If `block_start > pivot_index`, the block is "Right". Calculate `gap = block_start - pivot_index - 1`.
    *   Otherwise (adjacent or overlapping), the `gap = 0`. Ensure gap is non-negative.
9.  Calculate the `shift_amount`:
    *   If `gap == 0`, `shift_amount = 0`.
    *   If `gap == 1`, `shift_amount = 1`.
    *   If `gap > 1`, `shift_amount = 2`.
10. Calculate the `new_block_start` index for placing the block in the `output_list`:
    *   If the block was "Left", `new_block_start = block_start + shift_amount`.
    *   If the block was "Right", `new_block_start = block_start - shift_amount`.
    *   If the block was "Adjacent" (`gap == 0`), `new_block_start = block_start`.
11. Iterate through the `block_values`. For each value, determine its target index in the `output_list` (starting from `new_block_start` and incrementing). If the target index is valid (within bounds 0-11) and is *not* equal to `pivot_index`, place the value at that target index in the `output_list`.
12. Return the completed `output_list`.
"""

def find_pivot(sequence: List[int]) -> int:
    """Finds the index of the pivot element (2). Returns -1 if not found."""
    try:
        return sequence.index(2)
    except ValueError:
        return -1 # Pivot not found

def find_data_block(sequence: List[int], pivot_index: int) -> Optional[Tuple[int, int, List[int]]]:
    """
    Finds the first contiguous block of non-zero, non-pivot integers.
    Returns (start_index, end_index, values) or None if no block found.
    """
    block_start = -1
    block_values = []
    n = len(sequence)

    for i, val in enumerate(sequence):
        # Check if the current element qualifies as part of the data block
        is_block_element = (val != 0 and i != pivot_index)

        if is_block_element and block_start == -1:
            # Start of a potential block
            block_start = i
            block_values.append(val)
        elif is_block_element and block_start != -1:
            # Continuing an existing block
            block_values.append(val)
        elif not is_block_element and block_start != -1:
            # End of the block is detected (current element is 0 or pivot)
            block_end = i - 1
            return block_start, block_end, block_values

    # Handle case where block runs to the very end of the sequence
    if block_start != -1:
        block_end = n - 1
        return block_start, block_end, block_values

    # No block was found
    return None


def transform(input_grid) -> List[int]:
    # Convert input NumPy array (or potentially other iterable) to a Python list
    input_list = list(input_grid)
    n = len(input_list)
    
    # Ensure expected length, though maybe not strictly necessary if logic is sound
    if n != 12:
        print(f"Warning: Input sequence length is {n}, expected 12. Proceeding anyway.")
        
    # Initialize the output list with zeros
    output_list = [0] * n

    # Find the pivot index ('2')
    pivot_index = find_pivot(input_list)

    # Handle case where pivot is missing (return original list)
    if pivot_index == -1:
        print("Warning: Pivot '2' not found.")
        return input_list # Return original list if pivot is missing

    # Place the pivot in the output list; its position is fixed
    output_list[pivot_index] = 2

    # Find the data block (non-zero, non-pivot contiguous sequence)
    block_data = find_data_block(input_list, pivot_index)

    # If no data block exists, the output is just the pivot and zeros
    if block_data is None:
        return output_list

    # Unpack block data
    block_start, block_end, block_values = block_data

    # Determine block position relative to pivot and calculate the gap (number of zeros between)
    gap = 0
    relative_position = "Adjacent" # Default if block touches pivot index range
    if block_end < pivot_index:
        relative_position = "Left"
        gap = pivot_index - block_end - 1
    elif block_start > pivot_index:
        relative_position = "Right"
        gap = block_start - pivot_index - 1

    # Ensure gap is non-negative
    gap = max(0, gap)

    # Determine the shift amount based on the gap size
    shift_amount = 0
    if gap == 1:
        shift_amount = 1
    elif gap > 1:
        shift_amount = 2
    # else: shift_amount remains 0 for gap == 0

    # Calculate the starting index for the block in the output list
    new_block_start = block_start # Default to original position
    if relative_position == "Left":
        new_block_start += shift_amount
    elif relative_position == "Right":
        new_block_start -= shift_amount

    # Place the shifted data block into the output list
    current_output_idx = new_block_start
    for val in block_values:
        # Check if the target index is within bounds (0 to n-1)
        if 0 <= current_output_idx < n:
            # Crucially, only place the value if the target index is NOT the pivot's index
            if current_output_idx != pivot_index:
                output_list[current_output_idx] = val
        # else: Value would be shifted out of bounds, so it's omitted (based on examples)

        # Move to the next index for the next value in the block
        current_output_idx += 1

    # Return the final transformed list
    return output_list