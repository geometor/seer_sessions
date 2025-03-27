```python
import numpy as np
import math

"""
Transforms the input grid by identifying the bottom-most vertical contiguous block 
of red (2) pixels in each column. For each such identified block, it calculates 
its height 'H'. Then, it changes the color of the bottom floor(H / 2) pixels 
of that block to azure (8). If a column contains no red blocks, it remains unchanged.
"""

def _find_vertical_red_blocks(column_data):
    """
    Identifies contiguous vertical blocks of red (2) pixels in a column.

    Args:
        column_data (np.array): A 1D numpy array representing a single column.

    Returns:
        list: A list of tuples, where each tuple represents a block
              as (start_row, end_row). Returns an empty list if no red blocks are found.
    """
    blocks = []
    in_block = False
    start_row = -1
    red_color = 2

    for r, pixel in enumerate(column_data):
        if pixel == red_color and not in_block:
            # Start of a new block
            in_block = True
            start_row = r
        elif pixel != red_color and in_block:
            # End of the current block
            in_block = False
            blocks.append((start_row, r - 1))
            start_row = -1

    # Handle block ending at the last row
    if in_block:
        blocks.append((start_row, len(column_data) - 1))

    return blocks

def transform(input_grid):
    """
    Transforms the input grid based on vertical red blocks.

    Args:
        input_grid (list[list[int]]): The input grid.

    Returns:
        list[list[int]]: The transformed grid.
    """
    # Convert input_grid list of lists to numpy array for easier slicing
    input_array = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input
    output_array = np.copy(input_array)
    height, width = input_array.shape
    red_color = 2
    azure_color = 8

    # Iterate through each column
    for c in range(width):
        column_data = input_array[:, c]

        # Find all vertical contiguous blocks of red pixels in this column
        red_blocks = _find_vertical_red_blocks(column_data)

        # If no red blocks found in this column, continue to the next column
        if not red_blocks:
            continue

        # Select the red block that extends furthest down (highest end_row)
        bottom_most_block = max(red_blocks, key=lambda block: block[1])
        start_row, end_row = bottom_most_block

        # Calculate the height 'H' of this bottom-most block
        block_height = end_row - start_row + 1

        # Calculate the number of pixels 'C' to change: C = floor(H / 2)
        pixels_to_change = math.floor(block_height / 2)

        # Change the color of the bottom 'C' pixels of this block to azure
        # Iterate from i = 0 up to C - 1
        for i in range(pixels_to_change):
            # Calculate the row index of the pixel to change
            # Start from the bottom (end_row) and go up
            row_index = end_row - i
            # Ensure the row index is valid (should always be, but good practice)
            if 0 <= row_index < height:
                 # Change the pixel in the output grid
                output_array[row_index, c] = azure_color

    # Convert the output numpy array back to a list of lists
    return output_array.tolist()
```