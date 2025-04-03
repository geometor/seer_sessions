import numpy as np
from typing import List

"""
Transformation Rule:

1. Identify the single pivot pixel (maroon, 9) and its index in the 1D input grid.
2. Identify the contiguous block of identical non-white (0), non-pivot pixels. Note its color, length, and starting index.
3. In the output grid (initialized with white, 0), place the pivot pixel at its original index.
4. Place a single white separator pixel immediately to the right of the pivot pixel's index.
5. Place the identified colored block immediately to the right of the separator pixel, preserving its color and length.
"""

def find_pivot(input_list: List[int], pivot_color: int = 9) -> int:
    """Finds the index of the pivot color."""
    for i, color in enumerate(input_list):
        if color == pivot_color:
            return i
    raise ValueError(f"Pivot color {pivot_color} not found in input list.")

def find_block(input_list: List[int], pivot_color: int = 9, background_color: int = 0) -> tuple[int, int, int]:
    """Finds the contiguous block of non-background, non-pivot color."""
    block_color = -1
    block_start = -1
    block_length = 0
    in_block = False

    for i, color in enumerate(input_list):
        is_block_color = (color != background_color and color != pivot_color)

        if is_block_color and not in_block: # Start of a potential block
            in_block = True
            block_color = color
            block_start = i
            block_length = 1
        elif is_block_color and in_block: # Continuing a block
            if color == block_color:
                block_length += 1
            else: # Color changed, this shouldn't happen based on examples
                 raise ValueError("Unexpected change of color within a potential block.")
        elif not is_block_color and in_block: # End of the block
            # Found the block, return its properties
            return block_color, block_start, block_length

    # If the block runs to the end of the list
    if in_block:
        return block_color, block_start, block_length

    raise ValueError("No valid block found in input list.")


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid by moving a colored block from the left
    of a pivot pixel (maroon, 9) to its right, maintaining a single
    white pixel separator.
    """
    # Assume input is always 1xN
    if not input_grid or len(input_grid) != 1:
        raise ValueError("Input grid must be a 1xN grid.")

    input_list = input_grid[0]
    n = len(input_list)
    background_color = 0
    pivot_color = 9

    # Initialize output grid with background color
    output_list = [background_color] * n

    # Find the pivot pixel (maroon, 9)
    try:
        pivot_index = find_pivot(input_list, pivot_color)
    except ValueError as e:
        print(f"Error finding pivot: {e}")
        return [[background_color] * n] # Return empty grid on error

    # Find the colored block
    try:
        block_color, block_start, block_length = find_block(input_list, pivot_color, background_color)
    except ValueError as e:
        print(f"Error finding block: {e}")
        return [[background_color] * n] # Return empty grid on error

    # --- Construct the output grid ---

    # 1. Place the pivot pixel in the output at the same index
    if 0 <= pivot_index < n:
        output_list[pivot_index] = pivot_color
    else:
         print(f"Pivot index {pivot_index} out of bounds for grid length {n}.")
         return [[background_color] * n]

    # 2. Place the separator (white pixel) to the right of the pivot
    separator_index = pivot_index + 1
    if 0 <= separator_index < n:
        output_list[separator_index] = background_color # Already background, but explicit
    else:
        print(f"Separator index {separator_index} out of bounds. Cannot place separator.")
        # Maybe block cannot be placed either, proceed with caution or return error grid
        # For now, continue, but block placement might fail

    # 3. Place the colored block to the right of the separator
    output_block_start = separator_index + 1
    for i in range(block_length):
        current_index = output_block_start + i
        if 0 <= current_index < n:
            output_list[current_index] = block_color
        else:
            # This indicates the block would go out of bounds in the output
            print(f"Warning: Block placement index {current_index} out of bounds (grid length {n}). Truncating block.")
            break # Stop placing block pixels if out of bounds

    # Wrap the list back into the grid format
    output_grid = [output_list]
    return output_grid
