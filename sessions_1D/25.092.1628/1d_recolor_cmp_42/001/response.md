```python
"""
Change the color of the longest horizontal contiguous block(s) of green (3) pixels to maroon (9).
All other pixels retain their original color.
"""

import numpy as np

def find_contiguous_blocks(grid_row, target_color, row_index):
    """
    Finds contiguous horizontal blocks of a target color in a single grid row.

    Args:
        grid_row (np.array): A 1D numpy array representing a row of the grid.
        target_color (int): The color value to search for.
        row_index (int): The index of the row in the original grid.

    Returns:
        list: A list of tuples, where each tuple represents a block:
              (start_index, end_index, length, row_index).
              Returns an empty list if no blocks are found.
    """
    blocks = []
    start_index = -1
    for i, pixel in enumerate(grid_row):
        if pixel == target_color and start_index == -1:
            # Start of a new block
            start_index = i
        elif pixel != target_color and start_index != -1:
            # End of the current block
            end_index = i - 1
            length = end_index - start_index + 1
            blocks.append((start_index, end_index, length, row_index))
            start_index = -1 # Reset for the next block

    # Check if the last block extends to the end of the row
    if start_index != -1:
        end_index = len(grid_row) - 1
        length = end_index - start_index + 1
        blocks.append((start_index, end_index, length, row_index))

    return blocks

def transform(input_grid):
    """
    Transforms the input grid by changing the color of the longest horizontal
    contiguous block(s) of green (3) pixels to maroon (9).

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input grid to a numpy array for easier processing
    input_np = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_np)

    target_color = 3 # Green
    change_color = 9 # Maroon
    all_blocks = []

    # Iterate through each row to find green blocks
    for r_idx, row in enumerate(input_np):
        row_blocks = find_contiguous_blocks(row, target_color, r_idx)
        all_blocks.extend(row_blocks)

    # If no green blocks were found, return the original grid
    if not all_blocks:
        return output_grid.tolist()

    # Find the maximum length among all found green blocks
    max_length = 0
    for block in all_blocks:
        if block[2] > max_length:
            max_length = block[2]

    # Identify all blocks that have the maximum length
    longest_blocks = [block for block in all_blocks if block[2] == max_length]

    # Change the color of the pixels in the longest blocks
    for block in longest_blocks:
        start_col, end_col, _, row_idx = block
        # Modify the output grid in place
        output_grid[row_idx, start_col:end_col+1] = change_color

    # Convert the numpy array back to a list of lists for the final output
    return output_grid.tolist()
```