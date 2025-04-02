import sys
import math
import numpy as np # Using numpy for potential convenience, but core logic uses lists

# Define colors used in this task for clarity
WHITE = 0
MAGENTA = 6

"""
Transforms a 1D input grid by swapping a specific color block with its adjacent white space, bounded by a magenta barrier.

1.  Identifies the magenta pixel (6) which acts as a barrier, marking the end of the transformation zone.
2.  Within the zone before the barrier, locates the first contiguous block of pixels that are neither white (0) nor magenta (6) (the "movable block").
3.  Locates the contiguous block of white pixels (0) immediately following the movable block within the zone.
4.  Swaps the positions of the movable block and the adjacent white block.
5.  Pixels before the movable block (prefix), pixels between the white block and the barrier (intermediate), and pixels from the barrier onwards (suffix) remain in their relative positions.
6.  Reconstructs the grid row with the swapped blocks.
"""

def find_barrier_index(row):
    """Finds the index of the first occurrence of the MAGENTA barrier."""
    try:
        return row.index(MAGENTA)
    except ValueError:
        return -1 # Barrier not found

def find_movable_block(row, end_scan_idx):
    """
    Finds the start and end (exclusive) indices of the first contiguous block
    of non-WHITE, non-MAGENTA pixels within the row up to end_scan_idx.
    Returns (start_index, end_index_exclusive) or (-1, -1) if not found.
    """
    start_index = -1
    for i in range(end_scan_idx):
        pixel = row[i]
        # Start condition: Find the first non-white, non-magenta pixel
        if start_index == -1 and pixel != WHITE and pixel != MAGENTA:
            start_index = i
        # End condition: If we started a block, find where it ends
        elif start_index != -1:
            # Block ends if we hit white, magenta, the end_scan_idx, or a different non-white/non-magenta color
            if pixel == WHITE or pixel == MAGENTA or i == end_scan_idx or (pixel != WHITE and pixel != MAGENTA and pixel != row[start_index]):
                 return start_index, i

    # If a block started but reached the end_scan_idx without explicitly ending above
    if start_index != -1:
        return start_index, end_scan_idx

    return -1, -1 # Block not found

def find_adjacent_white_block(row, start_scan_idx, end_scan_idx):
    """
    Finds the start and end (exclusive) indices of the contiguous block of white pixels
    starting immediately at start_scan_idx within the row up to end_scan_idx.
    Returns (start_index, end_index_exclusive).
    If no white pixel at start_scan_idx, end_index_exclusive will equal start_scan_idx.
    """
    end_white_index = start_scan_idx
    for i in range(start_scan_idx, end_scan_idx):
        if row[i] == WHITE:
            end_white_index = i + 1
        else:
            break # Non-white pixel encountered, block ends
    # start_scan_idx is the start index for this block
    return start_scan_idx, end_white_index

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Assuming input_grid is a list containing a single list (the row)
    # or a NumPy array convertible to this structure.
    try:
      # Convert to list for consistent processing if it's numpy
      if isinstance(input_grid, np.ndarray):
          input_row = input_grid.tolist()[0]
      else:
          input_row = input_grid[0]
    except (IndexError, TypeError):
        # Handle cases where input_grid is empty or not structured as expected
        print("Warning: Input grid format unexpected or empty. Returning original.")
        return input_grid # Return original grid if format is wrong

    # 1. Find the barrier index
    barrier_idx = find_barrier_index(input_row)

    # If no barrier, the rule cannot be applied as defined by examples.
    if barrier_idx == -1:
        print("Warning: Magenta barrier (6) not found. Returning original grid.")
        return input_grid # Or handle as per specific requirements if barrier can be absent

    # Define the region where scanning/swapping occurs (before the barrier)
    scan_limit = barrier_idx

    # 2. Find the movable block
    movable_start, movable_end = find_movable_block(input_row, scan_limit)

    # If no movable block found before barrier, no swap needed.
    if movable_start == -1:
        print("Warning: Movable block not found before barrier. Returning original grid.")
        return input_grid # Return original grid

    # 3. Find the adjacent white block (starts immediately after the movable block)
    # white_start is conceptually movable_end
    white_start, white_end = find_adjacent_white_block(input_row, movable_end, scan_limit)

    # 4. Identify all segments based on found indices
    prefix = input_row[:movable_start]
    movable_block_content = input_row[movable_start:movable_end]
    # Use white_start and white_end found by the function
    white_block_content = input_row[white_start:white_end]
    intermediate_segment_content = input_row[white_end:scan_limit] # Pixels between white block end and barrier
    suffix = input_row[barrier_idx:] # Barrier and everything after it

    # 5. Reconstruct the output row by concatenating segments in the new order
    output_row = prefix + white_block_content + movable_block_content + intermediate_segment_content + suffix

    # 6. Return the result in the expected format (list of lists)
    output_grid = [output_row]

    return output_grid