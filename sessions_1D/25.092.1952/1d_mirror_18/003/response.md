```python
"""
Transformation Rule:
Identify a single maroon (9) pixel which acts as a pivot in a 1D grid.
Identify a contiguous block of a single color (not white 0 or maroon 9).
Move this colored block from one side of the pivot to the other, maintaining the same number of white (0) pixels (the gap) between the block and the pivot. The original position of the block becomes white (0) in the output grid. This implementation assumes the block initially appears before the pivot, as observed in all training examples.
"""

import numpy as np
from typing import Optional, Tuple

# Define colors for clarity
WHITE = 0
MAROON = 9

# --- Helper Functions ---

def find_pivot_np(grid: np.ndarray) -> Optional[int]:
    """Finds the index of the maroon (9) pivot pixel using NumPy."""
    indices = np.where(grid == MAROON)[0] # Find indices where the value is MAROON
    if indices.size > 0:
        return indices[0] # Return the first (and assumed only) occurrence
    return None # Pivot not found

def find_colored_block_np(grid: np.ndarray) -> Optional[Tuple[int, int, int, int]]:
    """
    Finds the contiguous block of color that is not white (0) or maroon (9) using NumPy.
    Assumes only one such block exists.
    Returns: (color, start_index, end_index, length) or None if not found.
    """
    grid_len = len(grid)
    for i in range(grid_len):
        pixel = grid[i]
        # Look for the start of a block (not white, not maroon)
        if pixel != WHITE and pixel != MAROON:
            start_index = i
            block_color = pixel
            # Find the end of the contiguous block of the same color
            end_index = start_index
            while end_index + 1 < grid_len and grid[end_index + 1] == block_color:
                end_index += 1
            # Calculate block length
            block_length = end_index - start_index + 1
            # Return block details - assumes only one block needs to be found
            return block_color, start_index, end_index, block_length
    return None # No suitable block found

# --- Main Transformation Function ---

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to move the colored block across the pivot
    in a 1D NumPy array.
    """
    grid_len = len(input_grid)

    # Initialize output grid with background color (white)
    output_grid = np.full(grid_len, WHITE, dtype=int)

    # Find the pivot
    pivot_index = find_pivot_np(input_grid)
    if pivot_index is None:
        print("Warning: Pivot (9) not found. Returning copy of input.")
        return np.copy(input_grid) # Return a copy if pivot is missing

    # Place the pivot in the output grid
    output_grid[pivot_index] = MAROON

    # Find the colored block
    block_info = find_colored_block_np(input_grid)
    if block_info is None:
        print("Warning: Colored block not found. Returning grid with only pivot.")
        return output_grid # Return grid with just the pivot if block is missing

    block_color, block_start_index, block_end_index, block_length = block_info

    # Calculate the gap and new position
    # This logic assumes the block is always BEFORE the pivot in the input,
    # based on the provided training examples.
    if block_end_index < pivot_index:
        # Calculate the gap size (number of white pixels between block end and pivot)
        gap = pivot_index - block_end_index - 1
        # Calculate the new starting index for the block (after pivot, preserving gap)
        new_start_index = pivot_index + 1 + gap
        new_end_index = new_start_index + block_length - 1
    else:
        # Handle the case where the block is AFTER the pivot (not seen in examples)
        # Calculate gap between pivot and block start
        gap = block_start_index - pivot_index - 1
        # Calculate new end index (before pivot, preserving gap)
        new_end_index = pivot_index - 1 - gap
        new_start_index = new_end_index - block_length + 1
        print(f"Warning: Block found after pivot at index {block_start_index}. Applying mirrored logic.")


    # Place the colored block in its new position in the output grid, checking bounds
    if 0 <= new_start_index < grid_len and 0 <= new_end_index < grid_len:
        output_grid[new_start_index : new_end_index + 1] = block_color
    else:
        # Handle error case: New position is out of bounds
        print(f"Warning: Calculated new block position ({new_start_index}-{new_end_index}) is out of bounds for grid length {grid_len}. Block not placed.")
        # Output grid will contain only the pivot in this case

    return output_grid
```