"""
Rearrange segments of a 1D input array based on identified patterns.
Specifically, it identifies:
1. An optional initial block of white pixels (prefix_whites).
2. The first contiguous block of non-white pixels following the prefix (main_block).
3. The first occurrence of a red (2) pixel after the main_block (separator_pixel).
4. An optional block of only white pixels located strictly between the main_block and the separator_pixel (intervening_whites).
5. The segment starting from the separator_pixel to the end (suffix).
The output is constructed by concatenating these segments in the order:
prefix_whites, intervening_whites, main_block, suffix.
"""

import numpy as np # Import numpy, although core logic will use lists

# --- Helper Functions ---

def find_prefix_whites_end(arr):
    """Finds the end index (exclusive) of the initial contiguous block of white (0) pixels."""
    end_index = 0
    # Use len() which works for both lists and numpy arrays
    while end_index < len(arr) and arr[end_index] == 0:
        end_index += 1
    return end_index

def find_first_non_white_block(arr, start_scan_index=0):
    """
    Finds the start (inclusive) and end (exclusive) indices of the first
    contiguous block of non-white pixels at or after start_scan_index.
    Returns (-1, -1) if no such block is found.
    """
    start = -1
    # Use len()
    for i in range(start_scan_index, len(arr)):
        if arr[i] != 0: # Found the start of a non-white block
            start = i
            # Now find the end of this block
            end = start + 1
            while end < len(arr) and arr[end] != 0:
                end += 1
            return start, end # Found the block, return its bounds
        # Keep scanning if current pixel is white
    return -1, -1 # No non-white block found

def find_first_occurrence(arr, value, start_scan_index=0):
    """
    Finds the index of the first occurrence of 'value' in 'arr'
    at or after start_scan_index. Returns -1 if not found.
    Works with lists and numpy arrays.
    """
    # Use len()
    try:
        for i in range(start_scan_index, len(arr)):
            if arr[i] == value:
                return i
        return -1
    except IndexError: # Catch if start_scan_index is out of bounds
         return -1

# --- Main Transformation Function ---

def transform(input_grid):
    """
    Applies the segment rearrangement transformation to the input grid (1D list or array).

    Args:
        input_grid: A list or numpy array of integers representing the input pixels.

    Returns:
        A list of integers representing the transformed output pixels.
    """
    # Ensure input is treated as a sequence (list or array both work with slicing and len)
    input_sequence = input_grid

    # 1. Identify prefix_whites
    prefix_whites_end = find_prefix_whites_end(input_sequence)
    prefix_whites = input_sequence[:prefix_whites_end]
    # print(f"Debug: prefix_whites = {list(prefix_whites)} (ends at {prefix_whites_end})")

    # 2. Identify main_block (first non-white block after prefix)
    main_block_start, main_block_end = find_first_non_white_block(input_sequence, prefix_whites_end)

    # Handle cases where no main block is found
    if main_block_start == -1:
        # The transformation rule requires a main block. If none, return original.
        # Convert to list if it's a numpy array for consistent output type
        return list(input_sequence)
    main_block = input_sequence[main_block_start:main_block_end]
    # print(f"Debug: main_block = {list(main_block)} (indices {main_block_start}-{main_block_end})")


    # 3. Identify separator_pixel index (first '2' after main_block)
    separator_index = find_first_occurrence(input_sequence, 2, main_block_end)

    # Handle cases where separator pixel is not found
    if separator_index == -1:
        # The transformation rule requires the separator pixel. If none, return original.
        return list(input_sequence)
    # print(f"Debug: separator_pixel (2) found at index {separator_index}")


    # 4. Identify intervening_whites (must be all '0' between main_block_end and separator_index)
    # Slicing works for both lists and numpy arrays
    intervening_segment = input_sequence[main_block_end:separator_index]
    intervening_whites = []
    # Explicitly check length and content, avoiding direct boolean check on segment itself
    if len(intervening_segment) > 0 and all(pixel == 0 for pixel in intervening_segment):
        intervening_whites = intervening_segment # Keep as slice/list for now
    # print(f"Debug: intervening_segment = {list(intervening_segment)}")
    # print(f"Debug: intervening_whites = {list(intervening_whites)}")


    # 5. Identify suffix (from separator_pixel to end)
    suffix = input_sequence[separator_index:]
    # print(f"Debug: suffix = {list(suffix)}")


    # 6. Construct the output list by concatenating segments
    # Convert segments to lists before concatenation to ensure correct behavior
    # regardless of whether input was list or np.array and how slices behave.
    output_list = list(prefix_whites) + list(intervening_whites) + list(main_block) + list(suffix)
    # print(f"Debug: final output = {output_list}")

    return output_list