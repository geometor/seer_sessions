import numpy as np
from typing import List, Tuple, Optional

"""
Examine the input, which consists of a single row of pixels.
Identify the contiguous segment (block) of non-white pixels. Note its color, its starting position (index), and its length.
Create a new output row of the same total length as the input row, filling it entirely with white pixels (color 0).
Copy the identified non-white block into this new row, but shift its starting position exactly one index to the right compared to its position in the input row. The color and length of the block must be identical to the input block.
"""

def find_contiguous_block(row: np.ndarray) -> Optional[Tuple[int, int, int]]:
    """
    Finds the first contiguous block of non-white pixels in a row.

    Args:
        row: A 1D numpy array representing pixel colors in the row.

    Returns:
        A tuple containing (block_color, start_index, length) if a block is found.
        Returns None if no non-white block is found.
    """
    start_index = -1
    block_color = -1
    length = 0
    in_block = False
    for i, pixel in enumerate(row):
        # Start of a new block
        if pixel != 0 and not in_block:
            start_index = i
            block_color = pixel
            length = 1
            in_block = True
        # Continuing the current block
        elif pixel == block_color and in_block:
            length += 1
        # End of the current block (hit a different color or white)
        elif pixel != block_color and in_block:
            # Found the first block, stop searching
            return int(block_color), start_index, length
    
    # If the loop finished and we were in a block (block goes to the end)
    if in_block:
         return int(block_color), start_index, length

    # No non-white block found
    return None


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid by shifting the contiguous non-white block 
    in the single row one position to the right.

    Args:
        input_grid: A numpy array representing the input grid (expected shape (1, N)).

    Returns:
        A numpy array representing the transformed grid.
    """
    # Ensure input is a numpy array
    input_grid = np.array(input_grid)

    # --- Input Validation and Extraction ---
    # Task assumes a single row input based on examples
    if input_grid.shape[0] != 1:
        # Return input or raise error if assumption is violated
        # For ARC, typically stick to observed patterns.
        # Returning an empty grid or the input might be options.
        # Let's assume valid input and extract the row.
        pass 
        
    input_row = input_grid[0]
    row_length = len(input_row)
    
    # --- Find the Object ---
    # Identify the contiguous block of non-white pixels.
    block_info = find_contiguous_block(input_row)

    # --- Initialize Output ---
    # Create a new row of the same length, filled with white pixels (0).
    # Using np.zeros handles the integer type and background color correctly.
    output_row = np.zeros(row_length, dtype=int)

    # --- Apply Transformation ---
    if block_info:
        block_color, start_index, block_length = block_info
        
        # Calculate the new starting index for the block (shifted right by 1).
        new_start_index = start_index + 1
        
        # Calculate the new ending index (exclusive) for slicing.
        new_end_index = new_start_index + block_length

        # Copy the block to the new position in the output row.
        # Ensure the block doesn't go out of bounds on the right.
        # Numpy slicing handles the end boundary correctly: if new_end_index
        # exceeds row_length, it will only fill up to the end.
        # We only need to ensure the start index is valid (which it should be
        # unless the block starts at the very last pixel and cannot be shifted).
        if new_start_index < row_length:
             # Determine the actual length to paint, considering boundary
             actual_length_to_paint = min(block_length, row_length - new_start_index)
             output_row[new_start_index : new_start_index + actual_length_to_paint] = block_color

    # --- Format Output ---
    # Return the transformed row wrapped in a 2D array structure.
    return np.array([output_row])