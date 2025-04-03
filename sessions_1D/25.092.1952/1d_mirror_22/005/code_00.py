import numpy as np
from typing import List, Tuple

"""
Moves a contiguous colored block within a 1D array across a separator pixel 
(maroon, 9), maintaining the relative distance (number of background pixels) 
between the block and the separator.

The transformation operates on a single 1D array (list of integers).
The block moves from its original side of the separator to the opposite side.
The separator's position remains unchanged.
The block's color and length remain unchanged.
The block's original position in the array is effectively replaced by the 
background color (white, 0) when the output array is initialized.
The relative distance (number of background pixels between block and separator) 
is preserved in the new position on the opposite side.
The block overwrites background pixels at its destination in the output array.
"""

def find_separator_index(row: np.ndarray) -> int:
    """Finds the index of the separator pixel (9) in a 1D row."""
    # Find indices where the value is 9
    separator_indices = np.where(row == 9)[0]
    # Validate that exactly one separator exists
    if len(separator_indices) != 1:
        raise ValueError(f"Expected exactly one separator pixel (9), found {len(separator_indices)}.")
    # Return the index of the single separator
    return separator_indices[0]

def find_colored_block(row: np.ndarray) -> Tuple[int, int, int]:
    """
    Finds the contiguous colored block (not 0 or 9) in a 1D row.

    Returns:
        A tuple containing (start_index, end_index, color).
    Raises:
        ValueError: If no block, multiple blocks, or inconsistent block found.
    """
    block_color = -1
    block_start = -1
    block_end = -1
    in_block = False
    found_block = False

    # Iterate through the row with index
    for i, pixel in enumerate(row):
        # Skip separator and background pixels
        if pixel == 9 or pixel == 0:
            if in_block:  # Just exited a block
                block_end = i - 1
                in_block = False
                # Since we expect only one block, we can stop searching
                break
            continue # Continue if not in a block and pixel is 0 or 9

        # Found a non-background, non-separator pixel
        current_pixel_color = pixel
        if not in_block:
            # Start of a new block
            if found_block:
                 raise ValueError("Found more than one colored block.") # Error if block already found previously
            block_color = current_pixel_color
            block_start = i
            in_block = True
            found_block = True
        elif current_pixel_color != block_color:
             # Error if inside a block but color changes
             raise ValueError(f"Found inconsistent color within a block. Expected {block_color}, got {current_pixel_color}.")

    # Handle case where block is at the very end of the row
    if in_block:
        block_end = len(row) - 1

    # Validate that a complete block was found
    if not found_block or block_start == -1 or block_end == -1:
        raise ValueError("Could not find a valid colored block.")

    return block_start, block_end, block_color


def transform(input_grid: List[int]) -> List[int]:
    """
    Applies the block-moving transformation to the input 1D grid.

    Args:
        input_grid: A list representing the 1D input grid.

    Returns:
        A list representing the 1D transformed grid.
    """
    # Convert input list to numpy array for efficient operations
    input_row = np.array(input_grid)
    grid_size = len(input_row)

    # Initialize output_row with background color (0)
    # This effectively handles clearing the original block's position
    output_row = np.zeros_like(input_row)

    # --- Transformation Steps ---

    # 1. Find the index of the separator (9)
    separator_index = find_separator_index(input_row)

    # 2. Place the separator in the output row at the same index
    output_row[separator_index] = 9

    # 3. Find the colored block (color C, start, end indices)
    block_start, block_end, block_color = find_colored_block(input_row)
    block_length = block_end - block_start + 1

    # 4. Determine if the block is to the left or right of the separator
    #    and calculate the distance (number of background cells between them)
    distance = 0
    is_left = block_end < separator_index
    if is_left:
        # Block is to the left. Distance = space between block_end and separator_index
        distance = separator_index - 1 - block_end
    else:
        # Block is to the right. Distance = space between separator_index and block_start
        distance = block_start - (separator_index + 1)

    # Ensure distance is non-negative (it should be based on logic)
    distance = max(0, distance)

    # 5. Calculate the new start and end indices for the block on the opposite side
    new_block_start = -1
    new_block_end = -1

    if is_left:
        # Block was left, move to right, maintaining distance
        new_block_start = separator_index + 1 + distance
        new_block_end = new_block_start + block_length - 1
    else:
        # Block was right, move to left, maintaining distance
        new_block_end = separator_index - 1 - distance
        new_block_start = new_block_end - block_length + 1

    # 6. Validate the calculated new position is within the grid bounds
    if new_block_start < 0 or new_block_end >= grid_size:
        raise ValueError(f"Calculated new block position [{new_block_start}, {new_block_end}] is out of bounds for grid size {grid_size}.")
    if new_block_start > new_block_end:
         raise ValueError(f"Calculated invalid block range: start {new_block_start} > end {new_block_end}")

    # 7. Place the block (using its color) into the calculated new position in the output row
    output_row[new_block_start : new_block_end + 1] = block_color

    # Convert the resulting numpy array back to a list for the return value
    output_grid = output_row.tolist()

    return output_grid