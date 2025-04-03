import numpy as np

"""
Transforms a 1D grid (list) by replacing contiguous blocks of yellow (4) pixels
based on their length, while keeping white (0) pixels unchanged.
- A block of 1 yellow pixel becomes 1 orange (7) pixel.
- A block of 2 yellow pixels becomes 2 maroon (9) pixels.
- A block of 3 yellow pixels becomes 3 red (2) pixels.
"""

def find_yellow_block_length(grid, start_index):
    """
    Finds the length of a contiguous block of yellow (4) pixels starting at a given index.
    
    Args:
        grid (list): The input grid (list of integers).
        start_index (int): The index where the yellow block starts.
        
    Returns:
        int: The length of the contiguous yellow block.
    """
    length = 0
    grid_len = len(grid)
    # Iterate from the start index as long as we are within bounds and the pixel is yellow
    for i in range(start_index, grid_len):
        if grid[i] == 4:
            length += 1
        else:
            # Stop counting when a non-yellow pixel is encountered
            break
    return length

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list): A list of integers representing the input pixel row.

    Returns:
        list: A list of integers representing the transformed output pixel row.
    """
    # Initialize output_grid as a copy of the input grid.
    # We will modify the yellow pixels in place.
    output_grid = list(input_grid)
    grid_len = len(input_grid)
    
    i = 0
    while i < grid_len:
        # Check if the current pixel is yellow
        if input_grid[i] == 4:
            # Find the length of the contiguous block of yellow pixels
            block_length = find_yellow_block_length(input_grid, i)
            
            # Determine the replacement color based on the block length
            output_color = -1 # Default or error value
            if block_length == 1:
                output_color = 7 # Orange
            elif block_length == 2:
                output_color = 9 # Maroon
            elif block_length == 3:
                output_color = 2 # Red
            # Add handling for unexpected lengths if necessary, 
            # though examples only show 1, 2, 3.
            # For now, assume only these lengths occur based on examples.
            
            # Fill the corresponding section in the output grid with the new color
            if output_color != -1:
                for j in range(i, i + block_length):
                    # Check bounds just in case, though logic should prevent overrun
                    if j < grid_len: 
                        output_grid[j] = output_color
            
            # Advance the index past the processed block
            i += block_length
        else:
            # If the pixel is not yellow (i.e., it's white), just move to the next pixel.
            # The white pixel is already correctly placed in the output_grid copy.
            i += 1
            
    return output_grid
