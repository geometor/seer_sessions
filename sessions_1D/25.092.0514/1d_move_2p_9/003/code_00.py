import numpy as np
from typing import List, Tuple, Optional

"""
Transforms a single-row input grid by identifying a contiguous block of a 
single non-white color and shifting this block two positions horizontally 
to the right. The space vacated by the block becomes white (0), and the 
background remains white. The block retains its original color and length.
The output grid has the same dimensions as the input grid.
"""

def find_contiguous_block(row: np.ndarray) -> Tuple[Optional[int], Optional[int], int]:
    """
    Finds the start index, color, and length of the first contiguous 
    non-white block in a 1D numpy array (row).

    Args:
        row: A 1D numpy array representing the input row.

    Returns:
        A tuple containing:
        - start_index (int or None): The starting index of the block, or None if no block found.
        - color (int or None): The color of the block, or None if no block found.
        - length (int): The length of the block (0 if no block found).
    """
    start_index = None
    color = None
    length = 0
    width = len(row)

    # Iterate through the row to find the first non-white pixel
    for i in range(width):
        if row[i] != 0:
            start_index = i
            color = row[i]
            break # Found the start of the block

    # If a block start was found, determine its length
    if start_index is not None:
        for i in range(start_index, width):
            if row[i] == color:
                length += 1
            else:
                break # End of the contiguous block of the same color

    return start_index, color, length

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule to the input grid.
    
    Identifies a contiguous non-white block in the single-row input grid 
    and shifts it two positions to the right in the output grid.

    Args:
        input_grid: A list containing a single list of integers representing the input row. 
                    It's assumed to be a single row based on examples.

    Returns:
        A list containing a single list of integers representing the transformed row.
    """
    # Validate input format - expect a list containing one list
    if not isinstance(input_grid, list) or len(input_grid) != 1 or not isinstance(input_grid[0], list):
         # In ARC context, returning the input might be safer than erroring if validation fails.
         # However, for clarity during development, an error is useful. 
         # Let's stick to raising error for now.
         raise ValueError("Input grid must be a list containing exactly one list (row).")

    # Extract the single row as a numpy array
    input_row = np.array(input_grid[0], dtype=int)
    width = len(input_row)

    # Initialize the output grid as a row filled with background color (0)
    output_row = np.zeros(width, dtype=int)

    # Find the non-white block details in the input row
    start_index, block_color, block_length = find_contiguous_block(input_row)

    # If a block was found, calculate its new position and place it in the output row
    if start_index is not None and block_color is not None:
        # Calculate the new starting position by shifting right by 2
        new_start_index = start_index + 2
        
        # Calculate the theoretical end index (exclusive)
        new_end_index = new_start_index + block_length

        # Place the block's color in the output grid within the calculated bounds,
        # ensuring we don't write outside the grid's width.
        # Iterate from the new start index up to the minimum of the new end index and the grid width.
        for i in range(new_start_index, min(new_end_index, width)):
             # Make sure the index is non-negative (it should be if new_start_index is)
             if i >= 0:
                 output_row[i] = block_color

    # Return the transformed row wrapped in a list to match ARC output format
    return [output_row.tolist()]