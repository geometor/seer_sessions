```python
"""
Identifies contiguous horizontal blocks of green (3) pixels in a 1D input grid.
Calculates the length of each block.
If the length is even, changes the block's pixels to blue (1) in the output grid.
If the length is odd, changes the block's pixels to gray (5) in the output grid.
White (0) pixels remain unchanged.
"""

import numpy as np

def find_contiguous_blocks(grid_1d, target_color):
    """
    Finds start index, end index, and length of contiguous blocks of a target color.

    Args:
        grid_1d (np.array): 1D NumPy array representing the grid row.
        target_color (int): The color value to search for.

    Returns:
        list: A list of tuples, where each tuple is (start_index, end_index, length).
              end_index is inclusive.
    """
    blocks = []
    i = 0
    n = len(grid_1d)
    while i < n:
        if grid_1d[i] == target_color:
            start_index = i
            # Find the end of the block
            while i < n and grid_1d[i] == target_color:
                i += 1
            end_index = i - 1
            length = end_index - start_index + 1
            blocks.append((start_index, end_index, length))
        else:
            i += 1
    return blocks

def transform(input_grid):
    """
    Transforms the input grid based on the length parity of contiguous green blocks.

    Args:
        input_grid (list): A 1D list representing the input grid row.

    Returns:
        list: A 1D list representing the transformed output grid row.
    """
    # Convert input to numpy array for easier processing
    # Assuming input_grid is a flat list representing a single row, as per examples
    grid_np = np.array(input_grid, dtype=int)

    # Initialize output grid as a copy of the input
    output_grid = grid_np.copy()

    # Define colors
    GREEN = 3
    BLUE = 1
    GRAY = 5

    # Find all contiguous blocks of green pixels
    green_blocks = find_contiguous_blocks(grid_np, GREEN)

    # Process each green block
    for start, end, length in green_blocks:
        # Determine the replacement color based on length parity
        if length % 2 == 0:  # Even length
            replacement_color = BLUE
        else:  # Odd length
            replacement_color = GRAY

        # Apply the replacement color to the corresponding segment in the output grid
        output_grid[start : end + 1] = replacement_color

    # Convert the numpy array back to a list for the final output
    return output_grid.tolist()
```