"""
Iterate through the input 1D grid. If a pixel is white (0), keep it white in the output. 
If a pixel is orange (7), identify the contiguous horizontal segment of orange pixels it belongs to. 
Determine the length of this segment. If the length is odd, change all pixels in that segment to red (2) in the output. 
If the length is even, change all pixels in that segment to magenta (6) in the output.
"""

import numpy as np

def find_segment_length(grid, start_index, color):
    """Finds the length of a contiguous segment of a given color starting at start_index."""
    length = 0
    n = len(grid)
    i = start_index
    while i < n and grid[i] == color:
        length += 1
        i += 1
    return length

def transform(input_grid):
    """
    Transforms the input grid based on the parity of the length of contiguous orange segments.

    Args:
        input_grid (list or np.array): A 1D list or array representing the input row.

    Returns:
        list: The transformed output row.
    """
    # Ensure input is a list for easier manipulation
    if isinstance(input_grid, np.ndarray):
        # Assuming input is 1D or a single row 2D array
        if input_grid.ndim > 1:
             input_list = input_grid.flatten().tolist()
        else:
             input_list = input_grid.tolist()
    else:
        # Handle potential nested lists if input represents a single row grid
        if isinstance(input_grid[0], list):
             input_list = list(input_grid[0])
        else:
             input_list = list(input_grid) # Make a copy if it's already a 1D list

    # Initialize output_grid as a copy of the input
    output_list = list(input_list)
    n = len(input_list)
    i = 0

    # Iterate through the input grid
    while i < n:
        # Check if the current pixel is orange
        if input_list[i] == 7:
            # Find the start and length of the contiguous orange segment
            start_index = i
            segment_length = find_segment_length(input_list, start_index, 7)
            end_index = start_index + segment_length # Index after the segment

            # Determine the output color based on length parity
            if segment_length % 2 != 0: # Odd length
                output_color = 2 # Red
            else: # Even length
                output_color = 6 # Magenta

            # Update the output list for the entire segment
            for j in range(start_index, end_index):
                output_list[j] = output_color

            # Advance the main loop index past this segment
            i = end_index
        else:
            # If the pixel is not orange (it's white 0), just move to the next pixel
            # White pixels are already correctly copied in output_list
            i += 1

    # Return the transformed list
    return output_list