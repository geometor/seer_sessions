import numpy as np

"""
Identifies a contiguous horizontal block of non-white pixels in the 1D input array 
(represented as a 1xN grid) and shifts this block 3 positions to the right in the 
output array. The space vacated by the shift and any space not covered by the 
shifted block is filled with the background color, white (0). The dimensions of 
the grid remain unchanged.
"""

def transform(input_grid):
    """
    Transforms the input grid by shifting the non-white horizontal block.

    Args:
        input_grid (list[list[int]]): A list containing a single list representing the 1D input grid.

    Returns:
        list[list[int]]: A list containing a single list representing the transformed 1D output grid.
    """
    # Ensure input is treated as a 1D array/row from the grid structure
    # ARC grids are list[list[int]]
    if not input_grid:
        return []
    input_row = np.array(input_grid[0], dtype=int)
    width = len(input_row)

    # Initialize output_row as a white row of the same dimensions
    output_row = np.zeros(width, dtype=int)

    # Find the first contiguous non-white block in the input row
    start_index = -1
    block_color = 0
    block_length = 0
    in_block = False

    for i, pixel in enumerate(input_row):
        if pixel != 0 and not in_block:  # Start of the block
            start_index = i
            block_color = pixel
            in_block = True
            block_length = 1
        elif pixel == block_color and in_block:  # Continuing the block
            block_length += 1
        elif pixel != block_color and in_block:  # End of the block (first non-matching pixel after block start)
            break  # Assume only one block based on examples
        # If pixel is 0 and not in_block, continue searching
        # If pixel is 0 and in_block, the loop would have already broken

    # If a non-white block was found
    if start_index != -1:
        # Calculate the new starting position for the block (shift right by 3)
        new_start_index = start_index + 3

        # Determine the actual range to place the block in the output, considering grid boundaries
        # Calculate the starting position for slicing, ensuring it's within bounds
        write_start = min(new_start_index, width)
        
        # Calculate the end position for slicing
        write_end = min(new_start_index + block_length, width)

        # Place the block into the output row if the new position is valid
        if write_start < write_end: # Ensure there's space to write
             output_row[write_start:write_end] = block_color

    # Format the output numpy array back into the list of lists structure expected by ARC
    output_grid = [output_row.tolist()]

    return output_grid