```python
"""
Transforms a 1xN input grid by relocating a contiguous colored block.
The transformation identifies a single pivot pixel (maroon 9) and a single
contiguous block of another color (not white 0 or maroon 9) that precedes the pivot.
The block is effectively 'cut' from its original position (which is then filled
with background color 0) and 'pasted' into the grid at a new location.
The new starting position of the block is determined by the original position
of the pivot and the length of the gap (sequence of pixels between the block
and the pivot in the input). Specifically, the block starts at index:
original_pivot_index + 1 + gap_length. The pivot pixel itself remains in its
original position.
"""

import numpy as np
from typing import List, Tuple, Dict, Any, Union

def find_pivot_index(row: List[int], pivot_color: int = 9) -> int:
    """Finds the index of the first occurrence of the pivot color."""
    for i, pixel in enumerate(row):
        if pixel == pivot_color:
            # Check if there's another pivot later
            if pivot_color in row[i+1:]:
                 raise ValueError("More than one pivot pixel found.")
            return i
    raise ValueError(f"Pivot color {pivot_color} not found.")

def find_colored_block(row: List[int], background_color: int = 0, pivot_color: int = 9) -> Tuple[List[int], int, int]:
    """
    Finds the first contiguous block of non-background, non-pivot color.

    Returns:
        Tuple[List[int], int, int]: (block_data, block_start_index, block_end_index)
    Raises:
        ValueError: If no block is found, or multiple/non-contiguous blocks are detected.
    """
    block_data = []
    block_start = -1
    block_end = -1
    in_block = False
    block_color = -1
    found_block = False # Flag to detect multiple blocks

    for i, pixel in enumerate(row):
        is_block_pixel = (pixel != background_color and pixel != pivot_color)

        if is_block_pixel:
            if not in_block: # Start of a new block
                if found_block:
                    # Found the start of a second block - error
                     raise ValueError("Multiple distinct colored blocks found.")
                block_start = i
                block_color = pixel
                in_block = True
                block_data.append(pixel)
                block_end = i
            elif in_block and pixel == block_color: # Continue the current block
                block_data.append(pixel)
                block_end = i
            elif in_block and pixel != block_color: # Different color adjacent to block
                 raise ValueError("Non-contiguous block or adjacent blocks of different colors found.")
        elif in_block: # End of the current block (hit background or pivot)
            in_block = False
            found_block = True # Mark that we have successfully found one block

    if not found_block:
        raise ValueError("Colored block not found.")

    return block_data, block_start, block_end


def transform(input_grid: Union[np.ndarray, List[List[int]]]) -> Union[np.ndarray, List[List[int]]]:
    """
    Applies the block relocation transformation to the input grid.

    Args:
        input_grid: A 1xN grid, represented as a numpy array or list of lists.

    Returns:
        The transformed 1xN grid in the same format as the input.
    """
    # --- Input Handling ---
    is_numpy = isinstance(input_grid, np.ndarray)
    if is_numpy:
        if input_grid.ndim == 1:
             input_list = [input_grid.tolist()]
        elif input_grid.ndim == 2:
             if input_grid.shape[0] != 1:
                 raise ValueError("Input grid must have exactly one row.")
             input_list = input_grid.tolist()
        else:
            raise ValueError("Input grid must be 1D or 2D.")
    elif isinstance(input_grid, list):
         if not input_grid or not isinstance(input_grid[0], list):
             # Try handling flat list input
             if all(isinstance(x, int) for x in input_grid):
                 input_list = [input_grid]
                 is_numpy = False # Treat as list of lists conceptually
             else:
                 raise TypeError("Input must be a list of lists or a flat list of integers.")
         elif len(input_grid) != 1:
             raise ValueError("Input grid must contain exactly one row.")
         else:
            input_list = input_grid
    else:
         raise TypeError("Input must be a numpy array or list of lists.")

    input_row = input_list[0]
    n_cols = len(input_row)
    if n_cols == 0: # Handle empty row
        return np.array([[]]) if is_numpy else [[]]

    background_color = 0
    pivot_color = 9

    try:
        # 1. Find Pivot
        pivot_index = find_pivot_index(input_row, pivot_color)

        # 2. Find Colored Block
        block_data, block_start, block_end = find_colored_block(input_row, background_color, pivot_color)

        # Validate block is before pivot
        if block_end >= pivot_index:
            raise ValueError("Colored block must precede the pivot pixel.")

        # 3. Calculate Gap Length
        gap_length = pivot_index - block_end - 1
        if gap_length < 0:
             # This implies block and pivot are adjacent, gap_length = -1, needs adjustment
             # Let's re-evaluate: pivot_index - (block_end + 1) gives number of elements between
             gap_length = max(0, pivot_index - (block_end + 1))


        # 4. Initialize Output Row as a copy
        output_row = list(input_row) # Use list() to ensure it's mutable

        # 5. Erase original block location in output row
        block_len = len(block_data)
        for i in range(block_start, block_end + 1):
            output_row[i] = background_color

        # 6. Calculate Target Start Index for the block
        target_block_start = pivot_index + 1 + gap_length

        # Check if target position is valid
        if target_block_start + block_len > n_cols:
            raise ValueError("Calculated target position for block exceeds grid boundaries.")

        # 7. Place block data at the target location
        for i in range(block_len):
            output_row[target_block_start + i] = block_data[i]

    except ValueError as e:
        # Handle errors like missing pivot/block or invalid configuration
        print(f"Warning: Input configuration error: {e}. Returning original grid.")
        # Returning the original grid might be required by ARC evaluation
        return input_grid


    # --- Output Formatting ---
    if is_numpy:
        # Use the original dtype if possible
        dtype = input_grid.dtype if hasattr(input_grid, 'dtype') else None
        output_grid = np.array([output_row], dtype=dtype)
    else:
         # Check original input format (list of lists vs flat list)
         if isinstance(input_grid, list) and isinstance(input_grid[0], list):
             output_grid = [output_row]
         else: # Assumed flat list originally
             output_grid = output_row

    return output_grid
```