import numpy as np
from typing import List

"""
Transformation Rule:
The input is a 2D grid, always observed as having 1 row and N columns in the examples (specifically 1x32).
The transformation operates horizontally along this single row.
It identifies contiguous blocks of non-white (non-zero) pixels.
If a block consists of a single pixel (length 1), it is replaced by a block of three pixels of the same color in the output row.
If a block consists of three pixels (length 3), it is kept unchanged (replaced by the same three pixels) in the output row.
White pixels (value 0) are preserved in their positions relative to the transformed blocks.
The output grid has the same dimensions as the input grid. The constructed output row replaces the input row.
"""

def find_block_length(row: np.ndarray, start_index: int, color: int) -> int:
    """
    Finds the length of a contiguous block of a given color starting at a specific index.

    Args:
        row: The 1D numpy array representing the row.
        start_index: The starting index to check from.
        color: The color of the block to measure.

    Returns:
        The length of the contiguous block.
    """
    length = 0
    n_cols = len(row)
    i = start_index
    while i < n_cols and row[i] == color:
        length += 1
        i += 1
    return length

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid according to the rule: expand non-white blocks of
    length 1 to length 3, keep blocks of length 3, and preserve white pixels.

    Args:
        input_grid: A 2D numpy array representing the input grid (expected shape (1, N)).

    Returns:
        A 2D numpy array representing the transformed grid with the same shape.
    """
    # Validate input shape (optional but good practice for ARC)
    if input_grid.shape[0] != 1:
        # Handle cases with more than one row if necessary,
        # but based on examples, we assume 1 row.
        # For now, let's raise an error or return input if shape is unexpected.
        # print(f"Warning: Expected input grid with 1 row, got {input_grid.shape[0]} rows.")
        # For this specific task based on examples, we proceed assuming 1 row.
        pass # Or raise ValueError("Input grid must have exactly one row for this task.")

    input_row = input_grid[0]
    n_cols = input_grid.shape[1]
    output_row_list = []
    i = 0 # Index for input_row

    # Iterate through the input row and build the output row list
    while i < n_cols:
        pixel_color = input_row[i]

        # Handle white pixels
        if pixel_color == 0:
            output_row_list.append(0)
            i += 1
        # Handle non-white blocks
        else:
            # Find the length of the contiguous block of this color
            block_color = pixel_color
            block_length = find_block_length(input_row, i, block_color)

            # Apply transformation based on block length
            if block_length == 1:
                # Expand block of length 1 to length 3
                output_row_list.extend([block_color] * 3)
            elif block_length == 3:
                # Keep block of length 3 as is
                output_row_list.extend([block_color] * 3)
            else:
                # Handle unexpected block lengths if needed.
                # Based on examples, only 1 and 3 occur.
                # If others occur, copy the block as is? Or error?
                # Let's assume examples cover all cases and copy as is for robustness.
                 output_row_list.extend([block_color] * block_length)


            # Advance the input index past the processed block
            i += block_length

    # Ensure the output row has the correct length (should match n_cols based on logic)
    # This check is more for verification during development.
    if len(output_row_list) != n_cols:
       # This might happen if an unexpected block length breaks the 1->3, 3->3 logic's
       # property of preserving total length. We might need to truncate or pad,
       # but let's assume the logic holds for valid inputs based on examples.
       # print(f"Warning: Output row length {len(output_row_list)} does not match input {n_cols}. Truncating/Padding.")
       # Simple truncation/padding:
       output_row_list = output_row_list[:n_cols]
       while len(output_row_list) < n_cols:
           output_row_list.append(0) # Pad with background color if needed

    # Create the output grid with the same shape as the input
    output_grid = np.zeros_like(input_grid)
    output_grid[0, :] = np.array(output_row_list, dtype=int)

    return output_grid
