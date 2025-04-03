import numpy as np
from typing import List

"""
Transformation Rule:
The input is a 1xN grid (a single row).
The transformation processes the row block by block, where a block is a contiguous sequence of pixels of the same color.
1. Identify the next block (color and length) starting from the current position.
2. If the block is non-white (color > 0):
   - If the block length is 1, append a block of the same color but length 3 to the output. Set a pending reduction of 2 for the next white block.
   - If the block length is 3, append a block of the same color and length 3 to the output. Set a pending reduction of 1 for the next white block.
   - (If other non-white lengths occur, copy the block as-is and set pending reduction to 0 - based on examples, only lengths 1 and 3 appear).
3. If the block is white (color == 0):
   - Calculate its effective length by subtracting the pending reduction (minimum length is 0).
   - Append a white block of this effective length to the output.
   - Reset the pending reduction to 0.
4. Repeat steps 1-3 until the entire input row is processed.
5. After processing, if the total length of the constructed output row is less than the input row length, append white pixels (0) to the end until the lengths match.
6. If the output row is longer (unlikely based on analysis), truncate it to match the input length.
7. The final result is a 1xN grid containing the transformed row.
"""

def find_block_length(row: np.ndarray, start_index: int) -> (int, int):
    """
    Finds the color and length of a contiguous block starting at a specific index.

    Args:
        row: The 1D numpy array representing the row.
        start_index: The starting index to check from.

    Returns:
        A tuple (color, length) of the contiguous block.
    """
    n_cols = len(row)
    if start_index >= n_cols:
        return (0, 0) # Should not happen in normal flow

    color = row[start_index]
    length = 0
    i = start_index
    while i < n_cols and row[i] == color:
        length += 1
        i += 1
    return color, length

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid according to the refined rule involving block expansion/preservation
    and subsequent white block reduction, ensuring output length matches input length.

    Args:
        input_grid: A 2D numpy array representing the input grid (expected shape (1, N)).

    Returns:
        A 2D numpy array representing the transformed grid with the same shape.
    """
    # Assume input is always 1xN based on examples
    if input_grid.shape[0] != 1:
        # Handle unexpected input shape if necessary, for now proceed assuming 1 row
        pass

    input_row = input_grid[0]
    n_cols = input_grid.shape[1]
    output_row_list = []
    pending_white_reduction = 0
    i = 0 # Current index in the input row

    # Iterate through the input row block by block
    while i < n_cols:
        # Find the next block's color and length
        block_color, block_length = find_block_length(input_row, i)

        if block_color == 0: # Current block is white
            # Calculate effective length after reduction
            effective_length = max(0, block_length - pending_white_reduction)
            # Append the reduced white block
            output_row_list.extend([0] * effective_length)
            # Reset the reduction needed for the *next* white block
            pending_white_reduction = 0
        else: # Current block is non-white
            original_length = block_length # Store original length for logic
            # Apply transformation based on original block length
            if original_length == 1:
                # Expand block of length 1 to length 3
                output_row_list.extend([block_color] * 3)
                # Set reduction for the next white block
                pending_white_reduction = 2
            elif original_length == 3:
                # Keep block of length 3 as is
                output_row_list.extend([block_color] * 3)
                # Set reduction for the next white block
                pending_white_reduction = 1
            else:
                # Handle unexpected non-white block lengths (e.g., copy as-is)
                # Based on examples, this case shouldn't be hit.
                output_row_list.extend([block_color] * original_length)
                pending_white_reduction = 0 # No reduction for unexpected lengths

        # Advance the input index past the processed block
        i += block_length

    # Adjust final length to match input length
    current_length = len(output_row_list)
    delta = n_cols - current_length

    if delta > 0:
        # Append white pixels if output is too short
        output_row_list.extend([0] * delta)
    elif delta < 0:
        # Truncate if output is too long (shouldn't happen based on analysis)
        output_row_list = output_row_list[:n_cols]

    # Create the output grid with the same shape as the input
    output_grid = np.zeros_like(input_grid)
    output_grid[0, :] = np.array(output_row_list, dtype=int)

    return output_grid