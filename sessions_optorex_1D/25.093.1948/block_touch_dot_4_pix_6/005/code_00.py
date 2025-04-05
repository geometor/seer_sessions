import sys
import math
# No special imports seem necessary for this logic

"""
Transformation Rule Natural Language Description:

1.  Receive the input sequence of digits (as a list, array, or similar iterable). Convert it into a standard list of integers if necessary.
2.  Find the index (`idx2`) of the unique digit `2` in the sequence. If `2` is not present, return the original sequence formatted as a space-separated string.
3.  Check Left Side:
    a.  Scan leftwards from `idx2 - 1` counting consecutive `0`s (`zeros_left_count`).
    b.  If `zeros_left_count > 0`:
        i.  Determine the potential end index of the non-zero block: `block_end_idx = idx2 - zeros_left_count - 1`.
        ii. Check if `block_end_idx` is valid (>= 0) and if the digit at this index (`grid[block_end_idx]`) is non-zero (`block_digit`).
        iii. If it is a non-zero digit, scan further left from `block_end_idx` to find the start index (`block_start_idx`) of the contiguous block of `block_digit`.
        iv. If a valid block (`block_digit > 0`) is confirmed to end exactly at `block_end_idx`:
            1.  Extract the sequence segments: `before_block` (elements up to `block_start_idx`), `the_zeros` (elements from `block_end_idx + 1` to `idx2 - 1`), `the_block` (elements from `block_start_idx` to `block_end_idx`), `marker_and_after` (elements from `idx2` onwards).
            2.  Reconstruct the sequence as `before_block + the_zeros + the_block + marker_and_after`.
            3.  Format the reconstructed sequence as a space-separated string and return it.
4.  Check Right Side (only if no change was made on the left):
    a.  Initialize `zeros_right_count = 0`. Scan rightwards from `idx2 + 1`. While the index is valid and the digit is `0`, increment `zeros_right_count` and move one step right.
    b.  If `zeros_right_count > 0`:
        i.  Determine the potential start index of the non-zero block: `block_start_idx = idx2 + zeros_right_count + 1`.
        ii. Check if `block_start_idx` is valid (< sequence length) and if the digit at this index (`grid[block_start_idx]`) is non-zero (`block_digit`).
        iii. If it is a non-zero digit, scan further right from `block_start_idx` to find the end index (`block_end_idx`) of the contiguous block of `block_digit`.
        iv. If a valid block (`block_digit > 0`) is confirmed to start exactly at `block_start_idx`:
            1.  Extract the sequence segments: `up_to_marker` (elements up to `idx2`), `the_zeros` (elements from `idx2 + 1` to `block_start_idx - 1`), `the_block` (elements from `block_start_idx` to `block_end_idx`), `after_block` (elements from `block_end_idx + 1` onwards).
            2.  Reconstruct the sequence as `up_to_marker + the_block + the_zeros + after_block`.
            3.  Format the reconstructed sequence as a space-separated string and return it.
5.  No Change: If neither the left nor the right pattern resulted in a transformation, format the original input sequence as a space-separated string and return it.
"""

def find_block_left(grid, end_idx):
    """
    Finds a contiguous block of identical non-zero digits ending at end_idx.
    Returns the block's digit, start index, and end index, or (None, -1, -1)
    if no such block exists or if the digit at end_idx is zero.
    """
    if end_idx < 0 or grid[end_idx] == 0:
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
    if start_idx >= n or grid[start_idx] == 0:
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

def transform(input_grid):
    """
    Applies the transformation rule to the input grid (sequence of digits).
    """
    # Convert input to a list of integers, handling potential non-string iterables
    try:
        # Attempt direct conversion if it's already an iterable of numbers/strings
        grid = [int(d) for d in input_grid]
    except (TypeError, ValueError):
        # Fallback if it's a single string needing split (less likely based on errors)
        try:
             grid = [int(d) for d in input_grid.split()]
        except Exception as e:
             # If input format is truly unexpected, return original or raise error
             print(f"Unexpected input format: {type(input_grid)}, value: {input_grid}. Error: {e}")
             # Returning original as string representation for robustness in testing
             return str(input_grid)


    n = len(grid)

    # Find the index of the marker '2'
    try:
        idx2 = grid.index(2)
    except ValueError:
        # '2' not found, return the original grid formatted as string
        return format_output(grid)

    # --- Check Left Side ---
    zeros_left_count = 0
    scan_idx = idx2 - 1
    # Scan leftwards for zeros immediately preceding '2'
    while scan_idx >= 0 and grid[scan_idx] == 0:
        zeros_left_count += 1
        scan_idx -= 1

    # If zeros were found, check for an adjacent non-zero block to their left
    if zeros_left_count > 0:
        block_end_check_idx = idx2 - zeros_left_count - 1
        if block_end_check_idx >= 0: # Check if there's space for a block
             # Find the block potentially ending at this position
             block_digit, block_start_idx, block_end_idx = find_block_left(grid, block_end_check_idx)
             # Verify that a valid non-zero block was found and it ends exactly where expected
             if block_digit is not None and block_end_idx == block_end_check_idx:
                # Perform the move: (elements before block) + (zeros) + (block) + (2 and elements after)
                segment_before_block = grid[:block_start_idx]
                # The zeros are located between the block end and index 2
                the_zeros = grid[block_end_idx + 1 : idx2]
                the_block = grid[block_start_idx : block_end_idx + 1]
                segment_from_2_onwards = grid[idx2:] # Includes the '2'

                # Reconstruct the grid
                output_grid = segment_before_block + the_zeros + the_block + segment_from_2_onwards
                return format_output(output_grid) # Return transformed result

    # --- Check Right Side (only if no change was made on the left) ---
    zeros_right_count = 0
    scan_idx = idx2 + 1
    # Scan rightwards for zeros immediately following '2'
    while scan_idx < n and grid[scan_idx] == 0:
        zeros_right_count += 1
        scan_idx += 1

    # If zeros were found, check for an adjacent non-zero block to their right
    if zeros_right_count > 0:
        block_start_check_idx = idx2 + zeros_right_count + 1
        if block_start_check_idx < n: # Check if there's space for a block
            # Find the block potentially starting at this position
            block_digit, block_start_idx, block_end_idx = find_block_right(grid, block_start_check_idx)
            # Verify that a valid non-zero block was found and it starts exactly where expected
            if block_digit is not None and block_start_idx == block_start_check_idx:
                 # Perform the move: (elements before 2, including 2) + (block) + (zeros) + (elements after block)
                 segment_up_to_2 = grid[:idx2 + 1] # Includes the '2'
                 # The zeros are located between index 2 and the block start
                 the_zeros = grid[idx2 + 1 : block_start_idx]
                 the_block = grid[block_start_idx : block_end_idx + 1]
                 segment_after_block = grid[block_end_idx + 1:]

                 # Reconstruct the grid
                 output_grid = segment_up_to_2 + the_block + the_zeros + segment_after_block
                 return format_output(output_grid) # Return transformed result

    # If no changes were made on either side, return the original grid formatted as string
    return format_output(grid)