"""
Recolors contiguous horizontal blocks of blue (1) pixels based on their length:
- Blocks of length 1 become azure (8).
- Blocks of length 2 become magenta (6).
- Blocks of length 3 become yellow (4).
White (0) pixels remain unchanged.
The input is treated as a 1D grid (a single row).
"""

import numpy as np

def find_contiguous_blocks(row, target_color):
    """
    Finds contiguous blocks of a specific color in a 1D array.

    Args:
        row (np.array): The 1D input array.
        target_color (int): The color value to find blocks of.

    Returns:
        list: A list of tuples, where each tuple represents a block
              and contains (start_index, length).
    """
    blocks = []
    n = len(row)
    i = 0
    while i < n:
        if row[i] == target_color:
            # Found the start of a potential block
            start_index = i
            length = 0
            # Count contiguous target_color pixels
            while i < n and row[i] == target_color:
                length += 1
                i += 1
            # Store the block information
            blocks.append((start_index, length))
        else:
            # Move to the next pixel if not the target color
            i += 1
    return blocks

def transform(input_grid):
    """
    Transforms the input grid by recoloring blocks of blue pixels based on length.

    Args:
        input_grid (list): A list representing the 1D input grid.

    Returns:
        list: The transformed 1D grid.
    """
    # Convert input list to a numpy array for easier handling
    # Assuming the input is always a flat list representing the 1D grid
    input_row = np.array(input_grid)

    # Initialize output_grid as a copy of the input
    output_row = input_row.copy()

    # Define the color mapping based on block length
    color_map = {
        1: 8,  # azure
        2: 6,  # magenta
        3: 4   # yellow
    }

    # Find all contiguous blocks of blue (1) pixels
    blue_blocks = find_contiguous_blocks(input_row, 1)

    # Iterate through the found blocks and apply the color transformation
    for start_index, length in blue_blocks:
        # Check if the length has a corresponding color in the map
        if length in color_map:
            new_color = color_map[length]
            # Recolor the block in the output row
            output_row[start_index : start_index + length] = new_color
        # Note: If a block length doesn't match 1, 2, or 3, it remains blue (1)
        # based on the examples, only lengths 1, 2, 3 seem to be recolored.

    # Convert the numpy array back to a list for the final output format
    return output_row.tolist()