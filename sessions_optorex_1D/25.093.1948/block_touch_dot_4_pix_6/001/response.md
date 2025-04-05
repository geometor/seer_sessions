```python
import sys
import math
# Add any other necessary imports here (e.g., numpy if needed for complex grid operations)

"""
Transformation Rule Natural Language Description:

1.  Find the index of the digit `2` in the input sequence.
2.  Check the segment immediately to the left of `2`. Scan leftwards, collecting consecutive `0`s (`intervening_zeros`).
3.  If `intervening_zeros` are found and they are immediately preceded by a non-zero digit `d`, identify the full block of `d` digits (`adjacent_block`).
4.  If such a block and zeros are found on the left, move the `intervening_zeros` to the position immediately before the start of the `adjacent_block`. Reconstruct and return the sequence.
5.  If no change was made on the left, check the segment immediately to the right of `2`. Scan rightwards, collecting consecutive `0`s (`intervening_zeros`).
6.  If `intervening_zeros` are found and they are immediately followed by a non-zero digit `d`, identify the full block of `d` digits (`adjacent_block`).
7.  If such a block and zeros are found on the right, move the `intervening_zeros` to the position immediately after the end of the `adjacent_block`. Reconstruct and return the sequence.
8.  If no changes were made on either side, return the original sequence.
"""

def find_block_left(grid, start_scan_idx):
    """
    Finds a contiguous block of identical non-zero digits ending at start_scan_idx.
    Returns the block's digit, start index, and end index, or None if no such block exists.
    """
    if start_scan_idx < 0 or grid[start_scan_idx] == 0:
        return None, -1, -1

    block_digit = grid[start_scan_idx]
    block_end_idx = start_scan_idx
    block_start_idx = block_end_idx
    while block_start_idx > 0 and grid[block_start_idx - 1] == block_digit:
        block_start_idx -= 1
    return block_digit, block_start_idx, block_end_idx

def find_block_right(grid, start_scan_idx):
    """
    Finds a contiguous block of identical non-zero digits starting at start_scan_idx.
    Returns the block's digit, start index, and end index, or None if no such block exists.
    """
    if start_scan_idx >= len(grid) or grid[start_scan_idx] == 0:
        return None, -1, -1

    block_digit = grid[start_scan_idx]
    block_start_idx = start_scan_idx
    block_end_idx = block_start_idx
    while block_end_idx < len(grid) - 1 and grid[block_end_idx + 1] == block_digit:
        block_end_idx += 1
    return block_digit, block_start_idx, block_end_idx


def transform(input_str):
    """
    Applies the transformation rule to the input string sequence.
    """
    # Parse input string into a list of integers
    grid = [int(d) for d in input_str.split()]
    n = len(grid)

    # Find the index of '2'
    try:
        idx2 = grid.index(2)
    except ValueError:
        # '2' not found, which shouldn't happen based on the problem description
        # Return original string as a fallback
        return input_str

    # --- Check Left Side ---
    num_zeros_left = 0
    scan_idx_left = idx2 - 1
    # Scan leftwards for zeros immediately preceding '2'
    while scan_idx_left >= 0 and grid[scan_idx_left] == 0:
        num_zeros_left += 1
        scan_idx_left -= 1

    # If zeros were found, check for an adjacent non-zero block
    if num_zeros_left > 0:
        block_digit_left, block_start_idx_left, block_end_idx_left = find_block_left(grid, scan_idx_left)
        # Ensure the block found is indeed adjacent (ends right before the zeros)
        if block_digit_left is not None and block_end_idx_left == idx2 - num_zeros_left - 1:
            # Perform the move: Move zeros from [block_end+1, idx2-1] to before block_start
            segment_before_block = grid[:block_start_idx_left]
            moved_zeros = grid[block_end_idx_left + 1 : idx2]
            the_block = grid[block_start_idx_left : block_end_idx_left + 1]
            segment_after_2 = grid[idx2:] # Includes the '2'

            # Reconstruct the grid
            new_grid = segment_before_block + moved_zeros + the_block + segment_after_2
            return " ".join(map(str, new_grid))

    # --- Check Right Side (only if no change was made on the left) ---
    num_zeros_right = 0
    scan_idx_right = idx2 + 1
    # Scan rightwards for zeros immediately following '2'
    while scan_idx_right < n and grid[scan_idx_right] == 0:
        num_zeros_right += 1
        scan_idx_right += 1

    # If zeros were found, check for an adjacent non-zero block
    if num_zeros_right > 0:
        block_digit_right, block_start_idx_right, block_end_idx_right = find_block_right(grid, scan_idx_right)
         # Ensure the block found is indeed adjacent (starts right after the zeros)
        if block_digit_right is not None and block_start_idx_right == idx2 + num_zeros_right + 1:
            # Perform the move: Move zeros from [idx2+1, block_start-1] to after block_end
            segment_before_2 = grid[:idx2 + 1] # Includes the '2'
            moved_zeros = grid[idx2 + 1 : block_start_idx_right]
            the_block = grid[block_start_idx_right : block_end_idx_right + 1]
            segment_after_block = grid[block_end_idx_right + 1:]

            # Reconstruct the grid
            new_grid = segment_before_2 + the_block + moved_zeros + segment_after_block
            return " ".join(map(str, new_grid))

    # If no changes were made on either side, return the original string
    return input_str

```