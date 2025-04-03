import numpy as np
from collections import Counter

"""
Transforms a 1D input grid by finding a single contiguous block of non-zero pixels.
This block is expected to contain exactly two colors: one 'marker' color appearing once,
and one 'body' color appearing multiple times.
If the marker pixel is found at the start (leftmost position) of the block,
it is moved to the end (rightmost position) of the block. The body pixels shift
leftwards to fill the gap.
The background (zero) pixels and the overall position of the block remain unchanged.
If the block structure is invalid or the marker is not at the start, the original grid is returned.
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
    # Find the actual end index by checking for breaks in contiguity from the start
    end_index = start_index
    while end_index + 1 < len(grid_1d) and grid_1d[end_index + 1] != 0:
        end_index += 1
        
    return start_index, end_index

def analyze_block(block):
    """
    Analyzes a block of pixels to find the marker and body colors and check structure.

    Args:
        block (np.array): The 1D numpy array representing the colored block.

    Returns:
        tuple: (marker_color, body_color, is_valid_structure)
               marker_color: The color appearing once (-1 if none/multiple).
               body_color: The color appearing multiple times (-1 if none/multiple).
               is_valid_structure: True if exactly one marker and one body color found, False otherwise.
    """
    if len(block) <= 1:
        return -1, -1, False # Block too small to have distinct marker/body

    color_counts = Counter(block)
    marker_color = -1
    body_color = -1
    marker_found = False
    body_found = False
    valid_structure = True

    # Check if there are exactly two distinct non-zero colors
    non_zero_colors = [c for c in color_counts if c != 0]
    if len(non_zero_colors) != 2:
        return -1, -1, False

    for color, count in color_counts.items():
        if color == 0: continue # Ignore background color if somehow included

        if count == 1:
            if marker_found: # Found more than one color with count 1
                valid_structure = False
                break
            marker_color = color
            marker_found = True
        elif count > 1:
            if body_found: # Found more than one color with count > 1
                valid_structure = False
                break
            body_color = color
            body_found = True
        # else: count is 0 or unexpected, handled by initial checks

    # Final structure check: need exactly one marker AND one body color
    if not (marker_found and body_found):
        valid_structure = False

    if not valid_structure:
        return -1, -1, False

    return marker_color, body_color, True


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
    
    # Initialize output_grid as a copy of the input, returned if transformation doesn't apply
    output_grid = np.copy(input_grid)

    # 1. Locate the Object: Find the contiguous non-white block
    start_index, end_index = find_colored_block_indices(input_grid)

    # If no block is found, return the original grid
    if start_index == -1:
        return output_grid.tolist() # Return as list

    # 2. Extract and Analyze the Object
    colored_block = input_grid[start_index : end_index + 1]
    block_len = len(colored_block)

    marker_color, body_color, is_valid_structure = analyze_block(colored_block)

    # If block structure is invalid, return the original grid
    if not is_valid_structure:
        return output_grid.tolist()

    # 3. Check the Condition: Marker must be at the start (index 0) of the block
    if colored_block[0] != marker_color:
        # Condition not met, return the original grid
        return output_grid.tolist()

    # 4. Perform Transformation
    # Create a new block filled with the body color
    new_block = np.full(block_len, body_color, dtype=int)
    # Place the marker color at the end
    new_block[-1] = marker_color

    # Place the reconstructed block back into the output grid
    output_grid[start_index : end_index + 1] = new_block

    # 5. Final Output: Return the modified grid as a list
    return output_grid.tolist()