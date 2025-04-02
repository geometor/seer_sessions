"""
Transforms an input 1D sequence (list) of integers based on the rule:
1. Find the first occurrence of the marker value 6.
2. Find the last contiguous block of a single non-zero color that occurs before the marker.
3. Identify the color of this block (the 'fill color').
4. Change all zero values (white pixels) located strictly between the end of this block and the marker's position to the 'fill color'.
5. Leave all other values unchanged.
"""

import copy
import numpy as np # Although not strictly necessary for this 1D case, useful for general ARC tasks

def find_marker_index(grid_1d):
    """
    Finds the index of the first occurrence of the marker value 6.

    Args:
        grid_1d: A list of integers representing the 1D grid.

    Returns:
        The index of the marker (6), or -1 if not found.
    """
    try:
        # Using list.index() finds the first occurrence
        return grid_1d.index(6)
    except ValueError:
        # Marker value 6 was not found in the list
        return -1

def find_fill_block_details(grid_1d, marker_idx):
    """
    Finds the end index and color of the relevant non-zero block before the marker.
    Searches backwards from the position just before the marker.

    Args:
        grid_1d: A list of integers representing the 1D grid.
        marker_idx: The index of the marker (6).

    Returns:
        A tuple (block_end_idx, fill_color), or (-1, -1) if no suitable block is found.
        block_end_idx: The index of the last element of the fill block.
        fill_color: The color (integer value) of the fill block.
    """
    block_end_idx = -1
    fill_color = -1

    # Search backwards from the index right before the marker
    for i in range(marker_idx - 1, -1, -1):
        if grid_1d[i] != 0: # Found the first non-zero element
            block_end_idx = i
            fill_color = grid_1d[i]
            break # Stop searching once the end of the relevant block is found

    return block_end_idx, fill_color

def transform(input_grid):
    """
    Applies the transformation rule to the input grid (1D list).

    Args:
        input_grid: A list of integers representing the input sequence.

    Returns:
        A new list of integers representing the transformed sequence.
        Returns a copy of the input if the transformation cannot be applied
        (e.g., no marker or no fill block found).
    """
    # Ensure input is a list (basic type checking)
    if not isinstance(input_grid, list):
        # Handle cases where input might not be a list as expected
        # Depending on the framework, might raise an error or try conversion
        # For now, returning input assuming it should have been a list
        print(f"Warning: Input was not a list, returning as is. Type: {type(input_grid)}")
        return copy.deepcopy(input_grid) # Return a copy to avoid modifying original if mutable

    # Initialize output_grid as a copy of the input to modify
    output_grid = list(input_grid) # Use list() for a shallow copy, sufficient here

    # 1. Locate the marker
    marker_idx = find_marker_index(output_grid)
    if marker_idx == -1:
        # No marker found, return the original grid copy
        return output_grid

    # 2. Locate the fill block end and its color
    block_end_idx, fill_color = find_fill_block_details(output_grid, marker_idx)
    if block_end_idx == -1:
        # No non-zero block found before the marker, return the original grid copy
        return output_grid

    # 3. Identify the gap segment
    # The gap starts at the index immediately after the block ends
    gap_start_idx = block_end_idx + 1
    # The gap ends at the index immediately before the marker
    gap_end_idx = marker_idx # The range endpoint is exclusive

    # 4. Modify the pixels within the gap
    # Iterate through the indices identified as the gap
    for i in range(gap_start_idx, gap_end_idx):
        # Check if the current pixel in the gap is white (0)
        if output_grid[i] == 0:
            # Change its color to the fill color
            output_grid[i] = fill_color

    # 5. Return the modified grid
    return output_grid