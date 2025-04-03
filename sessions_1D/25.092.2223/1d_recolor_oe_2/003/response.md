```python
"""
Recolor contiguous horizontal blocks of orange (7) pixels based on the parity of their length. If a block has an even length, change its pixels to azure (8). If a block has an odd length, change its pixels to gray (5). White (0) pixels remain unchanged. Assumes input is a single row (1D array or list).
"""

import numpy as np

def find_orange_blocks(grid_row):
    """
    Identifies contiguous blocks of orange (7) pixels in a 1D grid row.

    Args:
        grid_row (np.array): A NumPy array representing the grid row.

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
    Transforms the input grid row by changing the color of orange blocks
    based on the parity of their length.

    Args:
        input_grid (list or np.array): A list or NumPy array representing the input grid row.

    Returns:
        np.array: A NumPy array representing the transformed output grid row.
    """
    # Ensure input is a NumPy array for consistent handling
    input_np = np.array(input_grid, dtype=int)

    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_np)

    # Find all contiguous blocks of orange (7) pixels
    orange_blocks = find_orange_blocks(input_np)

    # Iterate through each identified block
    for start_index, end_index, length in orange_blocks:
        # Determine the new color based on the parity of the block length
        if length % 2 == 0:
            new_color = 8 # Azure for even length
        else:
            new_color = 5 # Gray for odd length

        # Change the color of the pixels within the block in the output grid
        # Use NumPy slicing for efficiency: output_grid[start:end+1]
        output_grid[start_index : end_index + 1] = new_color

    # Return the modified output grid as a NumPy array
    return output_grid
```