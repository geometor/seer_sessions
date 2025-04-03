"""
Change the color of contiguous horizontal blocks of orange (7) pixels within each row of the grid based on the parity of their length. If a block has an even length, change its pixels to azure (8). If a block has an odd length, change its pixels to gray (5). Pixels that are not part of an orange block remain unchanged.
"""

import numpy as np

def find_orange_blocks(grid_row):
    """
    Identifies contiguous blocks of orange (7) pixels in a 1D grid row.

    Args:
        grid_row (np.array): A 1D NumPy array representing the grid row.

    Returns:
        list: A list of tuples, where each tuple contains (start_index, end_index, length)
              for an identified orange block.
    """
    blocks = []
    i = 0
    n = len(grid_row)
    while i < n:
        # Check if the current pixel is orange (7)
        if grid_row[i] == 7:
            # Found the start of a potential block
            start_index = i
            # Find the end of the block
            j = i
            while j < n and grid_row[j] == 7:
                j += 1
            # end_index is the index of the last orange pixel in the block
            end_index = j - 1
            # Calculate the length of the block
            length = end_index - start_index + 1
            # Store the block information
            blocks.append((start_index, end_index, length))
            # Move the main index past the found block
            i = j
        else:
            # Move to the next pixel if not orange
            i += 1
    return blocks

def transform(input_grid):
    """
    Transforms the input grid by changing the color of horizontal orange blocks
    based on the parity of their length, operating row by row.

    Args:
        input_grid (np.array): A 2D NumPy array representing the input grid.

    Returns:
        np.array: A 2D NumPy array representing the transformed output grid.
    """
    # Ensure input is a NumPy array
    input_np = np.array(input_grid, dtype=int)

    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_np)

    # Get the number of rows in the grid
    num_rows = input_np.shape[0]

    # Iterate through each row of the input grid
    for r in range(num_rows):
        # Get the current row
        current_row = input_np[r, :]

        # Find all contiguous blocks of orange (7) pixels in the current row
        orange_blocks = find_orange_blocks(current_row)

        # Iterate through each identified block in this row
        for start_index, end_index, length in orange_blocks:
            # Determine the new color based on the parity of the block length
            if length % 2 == 0:
                new_color = 8 # Azure for even length
            else:
                new_color = 5 # Gray for odd length

            # Change the color of the pixels within the block in the output grid
            # Use NumPy slicing for the specific row: output_grid[r, start:end+1]
            output_grid[r, start_index : end_index + 1] = new_color

    # Return the modified output grid
    return output_grid