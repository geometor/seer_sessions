"""
Recolors contiguous horizontal blocks of blue (1) pixels within a single-row grid based on the length of the block.
- Blocks of length 1 become azure (8).
- Blocks of length 2 become magenta (6).
- Blocks of length 3 become yellow (4).
White (0) pixels remain unchanged.
The input and output are grids containing a single row (e.g., [[p1, p2, ...]]).
"""

import numpy as np

def find_contiguous_blocks(row, target_color):
    """
    Finds contiguous blocks of a specific color in a 1D array or list.

    Args:
        row (list or np.array): The 1D input row.
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
            # Continue search from the position after the block
            # i is already incremented correctly by the inner loop
        else:
            # Move to the next pixel if not the target color
            i += 1
    return blocks

def transform(input_grid):
    """
    Transforms the input grid by recoloring blocks of blue pixels based on length.

    Args:
        input_grid (list[list[int]]): A grid containing a single row.

    Returns:
        list[list[int]]: The transformed grid, also containing a single row.
    """
    # Extract the single row from the input grid structure
    # Assuming valid ARC input format: list containing one list
    if not isinstance(input_grid, list) or len(input_grid) != 1 or not isinstance(input_grid[0], list):
         # This case should ideally not happen with standard ARC tasks,
         # but added robustness for potential variations or testing setups.
         # Attempt to handle if input_grid is just a flat list.
         if isinstance(input_grid, list) and all(isinstance(x, int) for x in input_grid):
             input_row_list = input_grid
         else:
             # If format is truly unexpected, return input or raise error
             # For ARC, sticking to the expected [[...]] format is best.
             # Let's raise an error for clarity if the format is wrong.
             raise ValueError("Input grid format is not a list containing a single list of integers.")
    else:
        input_row_list = input_grid[0]


    # Convert the row list to a numpy array for easier manipulation
    input_row = np.array(input_row_list)

    # Initialize the output row as a copy of the input row
    output_row = input_row.copy()

    # Define the color mapping based on block length for blue blocks
    color_map = {
        1: 8,  # azure
        2: 6,  # magenta
        3: 4   # yellow
    }

    # Find all contiguous blocks of blue (1) pixels in the input row
    # The target color to find blocks of is blue (1)
    blue_blocks = find_contiguous_blocks(input_row, 1)

    # Iterate through the found blue blocks
    for start_index, length in blue_blocks:
        # Check if the length corresponds to a transformation rule in the color_map
        if length in color_map:
            # Get the new color from the map based on the block length
            new_color = color_map[length]
            # Recolor the segment in the output row corresponding to the block
            # using numpy slicing for efficiency
            output_row[start_index : start_index + length] = new_color
        # else: Blocks with lengths other than 1, 2, or 3 retain their original blue color (1)
        # because output_row started as a copy of input_row. No action needed for these.

    # Convert the final numpy array row back to a standard Python list
    output_row_list = output_row.tolist()

    # Wrap the output row list in another list to match the required output grid format
    output_grid = [output_row_list]

    # Return the transformed grid
    return output_grid