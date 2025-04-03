import copy
import numpy as np # Although not strictly needed for the list manipulation, it's often used in ARC contexts.

"""
Transforms a 1xN grid by finding a single maroon (9) marker pixel and a 
contiguous block of a single non-white(0), non-maroon(9) color located entirely 
to the left of the marker. The block is then moved ('reflected') to the right 
side of the marker such that the distance (number of cells) between the 
marker and the block's closest edge remains the same. The block's color and 
length are preserved. The marker's position remains unchanged. The original 
position of the block is filled with the background color (white, 0).

Natural Language Program:
1.  Create the output grid with the same dimensions as the input grid, filling it entirely with the background color (white, 0).
2.  Locate the single marker pixel (maroon, 9) in the input grid and record its index (`marker_idx`). If no marker is found, return a copy of the input grid.
3.  Place the marker pixel (maroon, 9) at `marker_idx` in the output grid.
4.  Search the input grid to the *left* of `marker_idx` for a contiguous block of pixels where all pixels have the same color, and that color is *not* white (0) and *not* maroon (9).
5.  If no such block is found to the left of the marker, return the output grid (which currently contains only the marker and the background).
6.  If a block is found, record its color (`block_color`), its length (`block_len`), and the index of its rightmost pixel (`block_right_idx_in`).
7.  Calculate the distance `d` representing the number of cells between the right edge of the block and the marker: `d = marker_idx - block_right_idx_in`.
8.  Calculate the starting index for the block in the output grid, placing it to the right of the marker with the same distance `d`: `output_start_idx = marker_idx + d`.
9.  Place the block into the output grid: Starting from `output_start_idx`, fill the next `block_len` cells with `block_color`. Ensure that placement does not go outside the grid boundaries.
10. Return the completed output grid.
"""

def find_marker(row):
    """
    Finds the index of the first occurrence of the marker (9) in a list.

    Args:
        row: A list of integers representing the grid row.

    Returns:
        The index of the marker (9), or -1 if not found.
    """
    try:
        return row.index(9)
    except ValueError:
        return -1 # Marker not found

def find_block_left_of_marker(row, marker_idx):
    """
    Finds the contiguous block of a single non-0, non-9 color located 
    entirely to the left of the marker index.

    Args:
        row: A list of integers representing the grid row.
        marker_idx: The index of the marker (9).

    Returns:
        A tuple: (block_color, block_len, block_right_idx).
        Returns (None, 0, -1) if no such block is found.
        - block_color: The color (int) of the found block.
        - block_len: The length (int) of the found block.
        - block_right_idx: The index (int) of the rightmost pixel of the block.
    """
    block_color = None
    block_right_idx = -1
    block_len = 0
    
    # Step 4 (part 1): Scan leftwards from marker_idx - 1 to find the right edge of the block.
    for i in range(marker_idx - 1, -1, -1):
        pixel = row[i]
        # Check if the pixel is part of a potential block (not background, not marker)
        if pixel != 0 and pixel != 9: 
            block_color = pixel 
            block_right_idx = i
            block_len = 1
            break # Found the rightmost pixel, stop this scan
            
    # If no block starting pixel found left of marker
    if block_color is None:
        return None, 0, -1 # Step 5 (handled implicitly by return)

    # Step 4 (part 2): Scan leftwards from block_right_idx - 1 to find the full extent (length)
    for i in range(block_right_idx - 1, -1, -1):
        # Check if the pixel extends the block (same color)
        if row[i] == block_color:
            block_len += 1
        else:
            # Block ended (different color or boundary)
            break 

    # Step 6 (implicit): Return the found block's properties
    return block_color, block_len, block_right_idx

def transform(input_grid):
    """
    Applies the block reflection transformation to the input grid.
    """
    # Validate input format - expecting list of lists (even for 1 row)
    if not isinstance(input_grid, list) or len(input_grid) == 0 or not isinstance(input_grid[0], list):
        print("Warning: Invalid input grid format.")
        # Return structure consistent with ARC (list of lists)
        return [[]] if not input_grid else copy.deepcopy(input_grid)
        
    input_row = input_grid[0]
    grid_width = len(input_row)

    # Handle empty row edge case
    if grid_width == 0:
        return [[]]

    # Step 1: Create the output grid (row) with the background color (white, 0).
    output_row = [0] * grid_width

    # Step 2: Locate the marker pixel (9) and record its index.
    marker_idx = find_marker(input_row)
    
    # Handle case where marker is not found (as per Step 2 instruction).
    if marker_idx == -1:
        print("Warning: Marker (9) not found. Returning input copy.")
        return copy.deepcopy(input_grid) 

    # Step 3: Place the marker pixel (9) at `marker_idx` in the output grid.
    output_row[marker_idx] = 9

    # Step 4 & 6: Search for the block left of the marker and get its properties.
    block_info = find_block_left_of_marker(input_row, marker_idx)
    block_color, block_len, block_right_idx_in = block_info

    # Step 5: If no block is found, return the output grid (marker + background).
    if block_color is None:
        return [output_row]

    # Step 7: Calculate the distance 'd'.
    distance = marker_idx - block_right_idx_in

    # Step 8: Calculate the starting index for the block in the output grid.
    output_start_idx = marker_idx + distance

    # Step 9: Place the block into the output grid.
    for i in range(block_len):
        current_idx = output_start_idx + i
        # Ensure placement is within grid bounds.
        if 0 <= current_idx < grid_width:
            # The logic (d >= 1) ensures output_start_idx > marker_idx,
            # so overwriting the marker at marker_idx is not expected.
            output_row[current_idx] = block_color
        # else: Implicitly handles truncation - parts outside bounds are ignored.

    # Step 10: Return the completed output grid (as a list containing the row).
    return [output_row]