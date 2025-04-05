import sys
import math
import numpy as np # Import numpy for handling potential ndarray inputs

"""
Transformation Rule Natural Language Description:

1.  Receive the input sequence of digits (potentially as a string, list, or NumPy array). Convert it into a flat, 1D list of integers (`grid`). Handle potential nesting (e.g., `[[...]]`).
2.  Find the index (`idx2`) of the unique digit `2` in the `grid`. If `2` is not found, return the `grid` formatted as a space-separated string.
3.  Check Left Side Pattern:
    a.  Scan leftwards from `idx2 - 1` counting consecutive `0`s (`zeros_left_count`).
    b.  If `zeros_left_count > 0`, check if there's a non-zero digit (`block_digit`) immediately preceding these zeros (at index `idx2 - zeros_left_count - 1`).
    c.  If such a `block_digit` exists, find the full contiguous block of this digit ending at that position (`block_start_idx`, `block_end_idx`).
    d.  If the pattern (Block - Zeros - 2) is confirmed, reconstruct the sequence: (elements before block) + (zeros) + (block) + (2 and elements after). Format as a string and return.
4.  Check Right Side Pattern (only if no change was made on the left):
    a.  Scan rightwards from `idx2 + 1` counting consecutive `0`s (`zeros_right_count`).
    b.  If `zeros_right_count > 0`, check if there's a non-zero digit (`block_digit`) immediately following these zeros (at index `idx2 + zeros_right_count + 1`).
    c.  If such a `block_digit` exists, find the full contiguous block of this digit starting at that position (`block_start_idx`, `block_end_idx`).
    d.  If the pattern (2 - Zeros - Block) is confirmed, reconstruct the sequence: (elements before 2, including 2) + (block) + (zeros) + (elements after block). Format as a string and return.
5.  No Change: If neither pattern triggered a reconstruction, format the original `grid` as a space-separated string and return it.
"""

def parse_input(input_data):
    """
    Parses various input formats (string, list, numpy array) into a 1D list of integers.
    Handles potential nesting like [[...]].
    """
    if isinstance(input_data, str):
        try:
            return [int(d) for d in input_data.split()]
        except ValueError:
             # Handle cases where string might not be space-separated digits
             print(f"Warning: Could not parse string input '{input_data}' as space-separated digits.")
             return [] # Or raise an error, depending on desired strictness
    elif isinstance(input_data, np.ndarray):
        # Flatten the array and convert elements to int
        return [int(d) for d in input_data.flatten()]
    elif isinstance(input_data, (list, tuple)):
        # Attempt to flatten if nested and convert
        try:
            if input_data and isinstance(input_data[0], (list, tuple, np.ndarray)):
                # Handle nested lists/tuples/arrays, assuming one level like [[...]]
                 flat_list = [item for sublist in input_data for item in sublist]
                 return [int(d) for d in flat_list]
            else:
                 # Assume it's already a flat list/tuple
                 return [int(d) for d in input_data]
        except (ValueError, TypeError) as e:
             print(f"Warning: Could not parse list/tuple input. Error: {e}. Input: {input_data}")
             return []
    else:
        print(f"Warning: Unhandled input type: {type(input_data)}. Input: {input_data}")
        return []


def find_block_left(grid, end_idx):
    """
    Finds a contiguous block of identical non-zero digits ending at end_idx.
    Returns the block's digit, start index, and end index, or (None, -1, -1)
    if no such block exists or if the digit at end_idx is zero.
    """
    if end_idx < 0 or end_idx >= len(grid) or grid[end_idx] == 0:
        return None, -1, -1

    block_digit = grid[end_idx]
    block_end_idx = end_idx
    block_start_idx = block_end_idx
    # Scan left to find the start of the block
    while block_start_idx > 0 and grid[block_start_idx - 1] == block_digit:
        block_start_idx -= 1
    return block_digit, block_start_idx, block_end_idx

def find_block_right(grid, start_idx):
    """
    Finds a contiguous block of identical non-zero digits starting at start_idx.
    Returns the block's digit, start index, and end index, or (None, -1, -1)
    if no such block exists or if the digit at start_idx is zero.
    """
    n = len(grid)
    if start_idx < 0 or start_idx >= n or grid[start_idx] == 0:
        return None, -1, -1

    block_digit = grid[start_idx]
    block_start_idx = start_idx
    block_end_idx = block_start_idx
    # Scan right to find the end of the block
    while block_end_idx < n - 1 and grid[block_end_idx + 1] == block_digit:
        block_end_idx += 1
    return block_digit, block_start_idx, block_end_idx

def format_output(grid):
    """Converts a list of integers to a space-separated string."""
    return " ".join(map(str, grid))

def transform(input_data):
    """
    Applies the transformation rule to the input grid (sequence of digits).
    """
    # --- Step 1 & 2: Parse Input and Find Marker '2' ---
    grid = parse_input(input_data)
    if not grid: # Handle empty list from parsing failure
        # Returning raw input string representation might be safest fallback
        return str(input_data) 

    n = len(grid)
    try:
        idx2 = grid.index(2)
    except ValueError:
        # '2' not found, return the original grid formatted as string
        return format_output(grid)

    # --- Step 3: Check Left Side Pattern ---
    zeros_left_count = 0
    scan_idx = idx2 - 1
    # Scan leftwards for zeros immediately preceding '2'
    while scan_idx >= 0 and grid[scan_idx] == 0:
        zeros_left_count += 1
        scan_idx -= 1

    # If zeros were found, check for an adjacent non-zero block to their left
    if zeros_left_count > 0:
        block_end_check_idx = idx2 - zeros_left_count - 1
        if block_end_check_idx >= 0: # Ensure there's space for a block
            # Find the block potentially ending at this position
            block_digit, block_start_idx, block_end_idx = find_block_left(grid, block_end_check_idx)
            # Verify that a valid non-zero block was found and it ends exactly where expected
            if block_digit is not None and block_end_idx == block_end_check_idx:
                # Perform the move: (before block) + (zeros) + (block) + (2 and after)
                segment_before_block = grid[:block_start_idx]
                the_zeros = grid[block_end_idx + 1 : idx2] # The zeros found
                the_block = grid[block_start_idx : block_end_idx + 1]
                segment_from_2_onwards = grid[idx2:] # Includes the '2'
                # Reconstruct and return
                output_grid = segment_before_block + the_zeros + the_block + segment_from_2_onwards
                return format_output(output_grid)

    # --- Step 4: Check Right Side Pattern (only if no change on left) ---
    zeros_right_count = 0
    scan_idx = idx2 + 1
    # Scan rightwards for zeros immediately following '2'
    while scan_idx < n and grid[scan_idx] == 0:
        zeros_right_count += 1
        scan_idx += 1

    # If zeros were found, check for an adjacent non-zero block to their right
    if zeros_right_count > 0:
        block_start_check_idx = idx2 + zeros_right_count + 1
        if block_start_check_idx < n: # Ensure there's space for a block
            # Find the block potentially starting at this position
            block_digit, block_start_idx, block_end_idx = find_block_right(grid, block_start_check_idx)
            # Verify that a valid non-zero block was found and it starts exactly where expected
            if block_digit is not None and block_start_idx == block_start_check_idx:
                # Perform the move: (up to 2) + (block) + (zeros) + (after block)
                segment_up_to_2 = grid[:idx2 + 1] # Includes the '2'
                the_zeros = grid[idx2 + 1 : block_start_idx] # The zeros found
                the_block = grid[block_start_idx : block_end_idx + 1]
                segment_after_block = grid[block_end_idx + 1:]
                # Reconstruct and return
                output_grid = segment_up_to_2 + the_block + the_zeros + segment_after_block
                return format_output(output_grid)

    # --- Step 5: No Change ---
    # If no changes were made on either side, return the original grid formatted
    return format_output(grid)