"""
Identifies the position of the azure pixel (8) in the input array.
Partitions the array into three segments: prefix (before 8), anchor (8), and suffix (after 8).
Within the prefix segment, separates white pixels (0) from non-white pixels, maintaining the relative order within each group.
Constructs the output array by concatenating the separated white prefix pixels, the non-white prefix pixels, the anchor pixel, and the suffix segment.
"""

import numpy as np # Although not strictly necessary for this list-based approach, it's good practice for ARC

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.

    Args:
        input_grid (list): A 1D list representing the input grid.

    Returns:
        list: A 1D list representing the transformed output grid.
    """
    # Ensure input is a list (or convert from numpy array if needed)
    if isinstance(input_grid, np.ndarray):
        # Assuming a 1xN or Nx1 numpy array
        input_list = input_grid.flatten().tolist()
    else:
        input_list = list(input_grid) # Make a copy if it's already a list

    # 1. Identify the position (index) of the azure pixel (color 8)
    try:
        anchor_index = input_list.index(8)
    except ValueError:
        # Handle case where anchor (8) is not found, though examples suggest it's always present
        return input_list # Or raise an error, or return a default

    # 2. Divide the input array into three segments
    prefix = input_list[:anchor_index]
    anchor = [input_list[anchor_index]] # Keep it as a list for concatenation
    suffix = input_list[anchor_index + 1:]

    # 3. Within the `prefix` segment, separate the elements into two groups
    prefix_zeros = []
    prefix_non_zeros = []
    for pixel in prefix:
        if pixel == 0:
            prefix_zeros.append(pixel)
        else:
            prefix_non_zeros.append(pixel)

    # 4. Construct the output array by concatenating the segments
    output_list = prefix_zeros + prefix_non_zeros + anchor + suffix

    # Return as a list (or convert back to numpy array if required by ARC framework)
    return output_list
