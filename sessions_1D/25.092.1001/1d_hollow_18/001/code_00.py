"""
Transforms a 1D input array by identifying contiguous blocks of non-white pixels (value > 0). 
For each block found, it keeps the first and last pixel of the block unchanged, 
and sets all pixels strictly between the first and last pixel to white (0). 
Pixels outside these blocks (white pixels) remain unchanged.
"""

import numpy as np # numpy is not strictly necessary for 1D, but good practice for ARC

def transform(input_grid):
    """
    Applies the block hollowing transformation to a 1D input grid.

    Args:
        input_grid (list or np.array): A 1D array of integers (colors).

    Returns:
        list: The transformed 1D array.
    """
    # Ensure input is a list for easier manipulation if it's numpy
    if isinstance(input_grid, np.ndarray):
        input_list = input_grid.tolist()
    else:
        input_list = list(input_grid) # Ensure it's a mutable list copy

    # Initialize output_grid as a copy of the input
    output_grid = list(input_list)
    n = len(input_list)
    i = 0

    # Iterate through the input array to find blocks
    while i < n:
        # Check if the current pixel is non-white (start of a potential block)
        if input_list[i] != 0:
            start_index = i
            block_color = input_list[i]
            
            # Find the end of this contiguous block of the same color
            j = i + 1
            while j < n and input_list[j] == block_color:
                j += 1
            # The block ends at index j-1
            end_index = j - 1

            # Hollow out the block if its length is greater than 2
            # Check if there are pixels *between* start and end
            if end_index > start_index + 1: 
                # Iterate from the pixel *after* the start_index 
                # up to (but not including) the end_index
                for k in range(start_index + 1, end_index):
                    output_grid[k] = 0 # Set interior pixels to white

            # Move the main iterator past the processed block
            # Start searching for the next block from index j
            i = j 
        else:
            # If the current pixel is white, just move to the next pixel
            i += 1

    return output_grid
