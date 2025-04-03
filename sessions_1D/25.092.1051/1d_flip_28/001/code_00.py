import numpy as np
from collections import Counter
import copy

"""
Transforms a single-row grid by swapping the positions of a single non-white pixel (singleton) and an adjacent contiguous block of another non-white color.

The transformation identifies the singleton pixel and the block based on their colors and contiguity. 
It then determines their relative positions (singleton left or right of the block).
Finally, it reconstructs the row by placing the block where the singleton was and the singleton where the block was, effectively swapping their locations while maintaining the block's internal structure and the surrounding white pixels.
"""

def find_objects(row):
    """
    Identifies the singleton pixel and the contiguous block in the row.

    Args:
        row: A 1D numpy array representing the input row.

    Returns:
        A tuple containing:
        s_idx (int): Index of the singleton pixel.
        s_color (int): Color of the singleton pixel.
        b_start (int): Start index of the block.
        b_end (int): End index of the block (inclusive).
        b_color (int): Color of the block.
        b_len (int): Length of the block.
        Returns None if objects cannot be identified as expected.
    """
    non_white_indices = np.where(row != 0)[0]
    if len(non_white_indices) < 2:
        return None # Not enough non-white pixels

    non_white_colors = row[non_white_indices]
    color_counts = Counter(non_white_colors)

    if len(color_counts) != 2:
        return None # Expected exactly two non-white colors

    s_color = -1
    b_color = -1
    for color, count in color_counts.items():
        if count == 1:
            s_color = color
        else:
            b_color = color

    if s_color == -1 or b_color == -1:
        return None # Failed to identify singleton and block colors

    s_idx = np.where(row == s_color)[0][0]
    block_indices = np.where(row == b_color)[0]

    # Check for contiguity of the block
    if not np.all(np.diff(block_indices) == 1):
        return None # Block pixels are not contiguous

    b_start = block_indices[0]
    b_end = block_indices[-1]
    b_len = len(block_indices)

    # Check for adjacency
    if s_idx != b_start - 1 and s_idx != b_end + 1:
        return None # Singleton is not adjacent to the block

    return s_idx, s_color, b_start, b_end, b_color, b_len


def transform(input_grid):
    """
    Applies the singleton-block swap transformation to the input grid.

    Args:
        input_grid: A 2D numpy array representing the input grid (expected 1xN).

    Returns:
        A 2D numpy array representing the transformed grid.
    """
    # Ensure input is a 2D numpy array
    if not isinstance(input_grid, np.ndarray):
        input_grid = np.array(input_grid)

    # Check if grid is single row
    if input_grid.shape[0] != 1:
        # Handle cases not matching the expected single row structure if necessary
        # For this task, we assume it's always a single row based on examples
        # If not, returning the original grid might be a safe default
        return input_grid

    # Make a copy to modify
    output_grid = copy.deepcopy(input_grid)
    row = output_grid[0]

    # Find the singleton and the block
    object_info = find_objects(row)

    if object_info is None:
        # If objects aren't found as expected, return the original grid
        return output_grid

    s_idx, s_color, b_start, b_end, b_color, b_len = object_info

    # Clear the original positions (optional, as we overwrite)
    # row[s_idx] = 0
    # row[b_start : b_end + 1] = 0

    # Perform the swap based on relative position
    if s_idx < b_start:
        # Singleton was to the left of the block
        # Place the block starting at the original singleton position
        row[s_idx : s_idx + b_len] = b_color
        # Place the singleton immediately after the new block position
        row[s_idx + b_len] = s_color
    else: # s_idx > b_end
        # Singleton was to the right of the block
        # Place the singleton at the original block start position
        row[b_start] = s_color
        # Place the block immediately after the new singleton position
        row[b_start + 1 : b_start + 1 + b_len] = b_color

    return output_grid
