```python
"""
Change the color of contiguous horizontal blocks of orange (7) pixels based on the parity of their length. If a block has an even length, change its pixels to azure (8). If a block has an odd length, change its pixels to gray (5). White (0) pixels remain unchanged.
"""

import numpy as np

def find_orange_blocks(grid_row):
    """
    Identifies contiguous blocks of orange (7) pixels in a 1D grid row.

    Args:
        grid_row (list): A list of integers representing the grid row.

    Returns:
        list: A list of tuples, where each tuple contains (start_index, end_index, length)
              for an identified orange block.
    """
    blocks = []
    i = 0
    n = len(grid_row)
    while i < n:
        if grid_row[i] == 7:
            # Found the start of a potential block
            start_index = i
            # Find the end of the block
            j = i
            while j < n and grid_row[j] == 7:
                j += 1
            end_index = j - 1 # inclusive index of the last 7
            length = end_index - start_index + 1
            blocks.append((start_index, end_index, length))
            i = j # Move index past the found block
        else:
            i += 1 # Move to the next pixel
    return blocks

def transform(input_grid):
    """
    Transforms the input grid row by changing the color of orange blocks
    based on the parity of their length.

    Args:
        input_grid (list): A list of integers representing the input grid row.

    Returns:
        list: A list of integers representing the transformed output grid row.
    """
    # Initialize output_grid as a copy of the input grid
    # Use list() to ensure it's a copy, not a reference
    output_grid = list(input_grid)

    # Find all contiguous blocks of orange (7) pixels
    orange_blocks = find_orange_blocks(input_grid)

    # Iterate through each identified block
    for start_index, end_index, length in orange_blocks:
        # Determine the new color based on the parity of the block length
        if length % 2 == 0:
            new_color = 8 # Azure for even length
        else:
            new_color = 5 # Gray for odd length

        # Change the color of the pixels within the block in the output grid
        for i in range(start_index, end_index + 1):
            output_grid[i] = new_color

    # Return the modified output grid
    return output_grid
```