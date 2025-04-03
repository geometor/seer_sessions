import numpy as np
from collections import Counter

"""
Transforms a 1D input grid by finding a single contiguous block of non-zero pixels.
This block is expected to contain exactly two colors: one 'marker' color appearing once,
and one 'body' color appearing multiple times.
If the marker pixel is found at the start (leftmost position) of the block,
it is moved to the end (rightmost position) of the block. The body pixels shift
leftwards to fill the gap, maintaining their order relative to each other.
The background (zero) pixels and the overall position of the block remain unchanged.
If the block structure or marker position doesn't match this expectation, the original grid is returned.
"""

def find_colored_block_indices(grid_1d):
    """
    Finds the start and end indices of the first contiguous block of non-zero pixels.

    Args:
        grid_1d (np.array): A 1D numpy array representing the input grid row.

    Returns:
        tuple: A tuple containing the start and end index (inclusive) of the block.
               Returns (-1, -1) if no non-zero block is found.
    """
    non_zero_indices = np.where(grid_1d != 0)[0]
    if len(non_zero_indices) == 0:
        return -1, -1  # No block found

    start_index = non_zero_indices[0]
    # Find the actual end index by checking for breaks in contiguity
    end_index = start_index
    while end_index + 1 < len(grid_1d) and grid_1d[end_index + 1] != 0:
        end_index += 1
        
    # Double check if the last detected non-zero index matches the contiguous block end
    if end_index != non_zero_indices[-1]:
        # This could indicate multiple blocks or scattered non-zero pixels.
        # Based on the problem, we assume a single contiguous block starting at the first non-zero.
        pass # Proceed with the contiguous block found from the start

    return start_index, end_index

def analyze_block(block):
    """
    Analyzes a block of pixels to find the marker and body colors.

    Args:
        block (np.array): The 1D numpy array representing the colored block.

    Returns:
        tuple: (marker_color, body_color) or (None, None) if the structure is invalid.
               Returns (-1, -1) if structure is invalid (not exactly one marker and one body color).
    """
    if len(block) <= 1:
        return -1, -1 # Block too small

    color_counts = Counter(block)
    marker_color = -1
    body_color = -1
    
    marker_found = False
    body_found = False

    for color, count in color_counts.items():
        if count == 1:
            if marker_found: return -1, -1 # Found more than one potential marker
            marker_color = color
            marker_found = True
        elif count > 1:
            if body_found: return -1, -1 # Found more than one potential body color
            body_color = color
            body_found = True
        else: # count == 0? Should not happen with non-zero blocks
             return -1, -1 

    if not marker_found or not body_found:
        return -1, -1 # Did not find exactly one marker AND one body color

    return marker_color, body_color


def transform(input_grid_list):
    """
    Applies the transformation rule to the input grid list.

    Args:
        input_grid_list (list): A list of integers representing the 1D input grid.

    Returns:
        list: The transformed grid as a list of integers.
    """
    # Convert list to numpy array for easier manipulation
    input_grid = np.array(input_grid_list, dtype=int)
    
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)

    # 1. Find the start and end indices of the non-zero block
    start_index, end_index = find_colored_block_indices(input_grid)

    # If no block is found, return the original grid
    if start_index == -1:
        return output_grid.tolist() # Return as list

    # 2. Extract the colored block
    colored_block = input_grid[start_index : end_index + 1]
    block_len = len(colored_block)

    # 3. Analyze the block to find marker and body colors
    marker_color, body_color = analyze_block(colored_block)

    # If block structure is invalid (not exactly one marker and one body color), return original
    if marker_color == -1 or body_color == -1:
        return output_grid.tolist()

    # 4. Check if the marker is at the start of the block
    if colored_block[0] != marker_color:
        # Condition not met (marker not at start), return original grid
        return output_grid.tolist()

    # 5. Construct the new block arrangement
    # Create a new block filled with the body color
    new_block = np.full(block_len, body_color, dtype=int)
    # Place the marker color at the end
    new_block[-1] = marker_color

    # 6. Place the reconstructed block back into the output grid
    output_grid[start_index : end_index + 1] = new_block

    # 7. Return the modified grid as a list
    return output_grid.tolist()