import numpy as np
import copy

"""
Identify all contiguous horizontal blocks of gray (5) pixels in the input grid.
Determine the maximum length among these gray blocks.
Change the color of all gray blocks that have this maximum length to green (3).
Leave all other pixels unchanged.
"""

def find_horizontal_blocks(row, color):
    """
    Finds contiguous horizontal blocks of a specific color in a 1D array (row).

    Args:
        row (np.array): A 1D numpy array representing a row of the grid.
        color (int): The color value to search for blocks of.

    Returns:
        list: A list of tuples, where each tuple represents a block and
              contains (start_index, end_index, length).
              Returns an empty list if no blocks are found.
    """
    blocks = []
    start_index = -1
    for i, pixel in enumerate(row):
        if pixel == color and start_index == -1:
            # Start of a potential block
            start_index = i
        elif pixel != color and start_index != -1:
            # End of the block
            end_index = i # end_index is exclusive in slicing later
            length = end_index - start_index
            blocks.append((start_index, end_index, length))
            start_index = -1 # Reset for next block
        # Handle block ending at the edge of the row
        if pixel == color and i == len(row) - 1 and start_index != -1:
             end_index = i + 1 # end_index is exclusive
             length = end_index - start_index
             blocks.append((start_index, end_index, length))

    return blocks


def transform(input_grid):
    """
    Identifies the longest horizontal contiguous block(s) of gray pixels (5)
    in each row and changes their color to green (3).

    Args:
        input_grid (list of lists or np.array): The input grid.

    Returns:
        np.array: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid_np)
    
    rows, cols = input_grid_np.shape

    # Since the examples are 1D (1 row), we process that row.
    # If it were 2D, we would loop through rows.
    # For now, assuming 1 row based on examples.
    if rows == 1:
        row_data = input_grid_np[0]

        # Find all gray blocks in the row
        gray_blocks = find_horizontal_blocks(row_data, 5)

        # Find the maximum length among the gray blocks
        max_length = 0
        if gray_blocks:
            max_length = max(block[2] for block in gray_blocks)

        # Transform the blocks with maximum length
        if max_length > 0:
            for start, end, length in gray_blocks:
                if length == max_length:
                    # Change the pixels in the output grid for this block
                    output_grid[0, start:end] = 3
    # else: # Potential future handling for multi-row grids
        # for r in range(rows):
        #   row_data = input_grid_np[r]
        #   ... process each row independently ... 
        #   (Note: The current logic assumes max length *within the row*,
        #    if it's max length *across the whole grid*, the logic needs adjustment)
        # For now, sticking to the observed 1D pattern.

    return output_grid.tolist() # Return as list of lists per ARC standard