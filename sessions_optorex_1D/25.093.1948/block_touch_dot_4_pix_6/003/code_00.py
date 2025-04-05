import sys
import math
# No special imports seem necessary for this logic

"""
Transformation Rule Natural Language Description:

1.  Receive the input sequence of digits as a space-separated string.
2.  Find the index (`idx2`) of the digit `2`.
3.  Check Left:
    a.  Scan leftwards from `idx2 - 1` counting consecutive `0`s (`zeros_left_count`).
    b.  If `zeros_left_count > 0`, check if the digit immediately preceding these zeros (`grid[idx2 - zeros_left_count - 1]`) is non-zero (`block_digit`).
    c.  If a non-zero `block_digit` is found, identify the full contiguous block of this digit ending at that position (`block_start_idx`, `block_end_idx`).
    d.  If the full pattern (Block - Zeros - 2) is confirmed, reconstruct the sequence: (elements before block) + (zeros) + (block) + (2 and elements after). Return the result as a space-separated string.
4.  Check Right (only if no change was made in step 3):
    a.  Scan rightwards from `idx2 + 1` counting consecutive `0`s (`zeros_right_count`).
    b.  If `zeros_right_count > 0`, check if the digit immediately following these zeros (`grid[idx2 + zeros_right_count + 1]`) is non-zero (`block_digit`).
    c.  If a non-zero `block_digit` is found, identify the full contiguous block of this digit starting at that position (`block_start_idx`, `block_end_idx`).
    d.  If the full pattern (2 - Zeros - Block) is confirmed, reconstruct the sequence: (elements before 2, including 2) + (block) + (zeros) + (elements after block). Return the result as a space-separated string.
5.  If no changes were made in steps 3 or 4, return the original input string.
"""

def find_block_left(grid, end_idx):
    """
    Finds a contiguous block of identical non-zero digits ending at end_idx.
    Returns the block's digit, start index, and end index, or None if no such block exists
    or if the digit at end_idx is zero.
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
    Returns the block's digit, start index, and end index, or None if no such block exists
    or if the digit at start_idx is zero.
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


def transform(input_str):
    """
    Applies the transformation rule to the input sequence string.
    """
    # Parse input string into a list of integers
    # Assuming input is a space-separated string of digits.
    # If input_str is actually already a list/array, this line needs adjustment.
    try:
        grid = [int(d) for d in input_str.split()]
    except AttributeError:
         # If input is not a string (e.g., numpy array passed by test harness)
         # try converting elements to int directly.
         # This handles the error seen previously.
         grid = [int(d) for d in input_str]
         
    n = len(grid)
    output_grid = list(grid) # Make a copy to modify potentially

    # --- Find the marker '2' ---
    try:
        idx2 = grid.index(2)
    except ValueError:
        # '2' not found, return original string representation
        return " ".join(map(str, grid))

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
        if block_end_check_idx >= 0: # Ensure there's space for a block
             block_digit, block_start_idx, block_end_idx = find_block_left(grid, block_end_check_idx)
             # Check if a valid block was found ending exactly where expected
             if block_digit is not None and block_end_idx == block_end_check_idx:
                # Perform the move: (elements before block) + (zeros) + (block) + (2 and elements after)
                segment_before_block = grid[:block_start_idx]
                moved_zeros = grid[block_end_idx + 1 : idx2] # The zeros found
                the_block = grid[block_start_idx : block_end_idx + 1]
                segment_from_2_onwards = grid[idx2:] # Includes the '2'

                # Reconstruct the grid
                output_grid = segment_before_block + moved_zeros + the_block + segment_from_2_onwards
                return " ".join(map(str, output_grid)) # Return transformed result

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
        if block_start_check_idx < n: # Ensure there's space for a block
            block_digit, block_start_idx, block_end_idx = find_block_right(grid, block_start_check_idx)
            # Check if a valid block was found starting exactly where expected
            if block_digit is not None and block_start_idx == block_start_check_idx:
                 # Perform the move: (elements before 2, including 2) + (block) + (zeros) + (elements after block)
                 segment_up_to_2 = grid[:idx2 + 1] # Includes the '2'
                 moved_zeros = grid[idx2 + 1 : block_start_idx] # The zeros found
                 the_block = grid[block_start_idx : block_end_idx + 1]
                 segment_after_block = grid[block_end_idx + 1:]

                 # Reconstruct the grid
                 output_grid = segment_up_to_2 + the_block + moved_zeros + segment_after_block
                 return " ".join(map(str, output_grid)) # Return transformed result

    # If no changes were made on either side, return the original grid as a string
    return " ".join(map(str, grid))