import numpy as np
from typing import List, Tuple, Dict, Set

# Define color constants based on the problem description (though not strictly needed for the logic)
WHITE = 0
BLUE = 1
RED = 2
GREEN = 3
YELLOW = 4
GRAY = 5
MAGENTA = 6
ORANGE = 7
AZURE = 8
MAROON = 9

BACKGROUND_COLOR = WHITE
TARGET_COLOR = GREEN
EXCLUDED_COLORS_FOR_BLOCK = {BACKGROUND_COLOR, TARGET_COLOR}

def find_pixel(grid: List[int], color: int) -> int:
    """Finds the index of the first pixel with the specified color."""
    for i, pixel_color in enumerate(grid):
        if pixel_color == color:
            return i
    raise ValueError(f"Color {color} not found in grid")

def find_block(grid: List[int], exclude_colors: Set[int]) -> Tuple[int, int, int]:
    """
    Finds the start index, end index, and color of the first contiguous block
    of pixels whose color is not in the exclude_colors set.
    """
    start_index = -1
    block_color = -1
    for i, pixel_color in enumerate(grid):
        if pixel_color not in exclude_colors:
            if start_index == -1:
                start_index = i
                block_color = pixel_color
            # Check if the color is consistent within the block
            elif pixel_color != block_color:
                # This indicates the end of the block we were tracking
                 return start_index, i - 1, block_color
        elif start_index != -1:
            # We were tracking a block, and now it ended
            return start_index, i - 1, block_color

    # If the block extends to the end of the grid
    if start_index != -1:
        return start_index, len(grid) - 1, block_color

    raise ValueError("No movable block found in grid")


def transform(input_grid_list: List[int]) -> List[int]:
    """
    Transforms the input grid (1D list of integers) according to the rule:
    1. Identify the unique green pixel (target_pixel, color 3).
    2. Identify the contiguous block of non-white, non-green pixels (moving_block).
    3. Calculate the gap (number of white pixels) between the moving_block and the target_pixel.
    4. Shift the moving_block rightwards by the gap size so its right edge is adjacent
       to the target_pixel's left side.
    5. Fill the positions vacated by the shift with the background color (white, 0).
    """
    # Ensure input is a list for mutability
    input_grid = list(input_grid_list)

    # 1. Identify the target pixel (green)
    try:
        target_idx = find_pixel(input_grid, TARGET_COLOR)
    except ValueError:
        print("Warning: Target color (GREEN) not found. Returning input grid.")
        return input_grid # Or handle error appropriately

    # 2. Identify the moving block
    try:
        block_start, block_end, block_color = find_block(input_grid, EXCLUDED_COLORS_FOR_BLOCK)
    except ValueError:
        print("Warning: Movable block not found. Returning input grid.")
        return input_grid # Or handle error appropriately

    # 3. Calculate the gap size
    # gap = position_of_target - position_of_block_end - 1
    gap = target_idx - block_end - 1

    # Check if the block is already in the correct position or needs to move
    if gap < 0:
        print("Warning: Block is already past or overlapping the target. Returning input grid.")
        return input_grid # Block is already past or overlapping target
    if gap == 0:
         return input_grid # Block is already in the correct position

    # 4. Create the output grid initially as a copy of the input
    output_grid = list(input_grid)
    block_length = block_end - block_start + 1

    # 5. Shift the moving_block rightwards and fill vacated space

    # First, set the vacated area (leftmost 'gap' cells of the original block position) to background color
    # These are the cells that will be "left behind" after the shift.
    for i in range(block_start, block_start + gap):
         if i < len(output_grid): # Boundary check
              output_grid[i] = BACKGROUND_COLOR

    # Second, place the block's pixels in their new positions
    # Iterate through the original block positions
    for i in range(block_length):
        original_idx = block_start + i
        new_idx = original_idx + gap # Calculate the new position after shifting by 'gap'

        # Make sure the new index is within grid bounds
        if new_idx < len(output_grid):
            # The color comes from the original block's color
            output_grid[new_idx] = block_color
        else:
            # This case shouldn't happen if logic is correct and grid is large enough,
            # but added as a safeguard.
            print(f"Warning: New index {new_idx} out of bounds for grid length {len(output_grid)}")


    return output_grid