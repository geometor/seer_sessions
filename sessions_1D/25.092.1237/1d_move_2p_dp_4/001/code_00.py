import numpy as np
from typing import List, Tuple, Optional

# Define colors for clarity, though only numeric values are used in the logic
COLOR_MAP = {
    0: "white",
    1: "blue",
    2: "red",
    3: "green",
    4: "yellow",
    5: "gray",
    6: "magenta",
    7: "orange",
    8: "azure",
    9: "maroon",
}
WHITE = 0
AZURE = 8

def find_colored_block(grid: List[int]) -> Optional[Tuple[int, int, int]]:
    """
    Finds the contiguous horizontal block of pixels that are not white (0) and not azure (8).

    Args:
        grid: A 1D list representing the input grid row.

    Returns:
        A tuple containing (start_index, end_index, color) of the block,
        or None if no such block is found.
    """
    start_index = -1
    block_color = -1
    for i, pixel in enumerate(grid):
        if pixel != WHITE and pixel != AZURE:
            if start_index == -1:
                start_index = i
                block_color = pixel
            # Continue if the pixel matches the block color
            elif pixel != block_color:
                # Found the end of the block because the color changed
                return start_index, i - 1, block_color
        elif start_index != -1:
            # Found the end of the block because we hit white or azure
            return start_index, i - 1, block_color

    # Check if the block extends to the end of the grid
    if start_index != -1:
        return start_index, len(grid) - 1, block_color

    return None # No block found

def find_anchor_pixel(grid: List[int]) -> Optional[int]:
    """
    Finds the index of the azure (8) pixel.

    Args:
        grid: A 1D list representing the input grid row.

    Returns:
        The index of the azure pixel, or None if not found.
    """
    for i, pixel in enumerate(grid):
        if pixel == AZURE:
            return i
    return None

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid according to the following rules:
    1. Identifies a contiguous horizontal block of a single color (not white 0 or azure 8).
    2. Identifies a single azure (8) anchor pixel.
    3. Shifts the colored block horizontally to the right so that its rightmost pixel
       is immediately adjacent (left) to the azure anchor pixel.
    4. Fills the original position of the block with white (0) pixels.
    5. The anchor pixel and other background pixels remain in their positions unless
       overwritten by the shifted block.
    """
    # Ensure input is treated as a 1D list
    if input_grid.ndim > 1 and input_grid.shape[0] != 1:
        raise ValueError("Input grid must be 1D or have height 1")
    input_list = input_grid.flatten().tolist()
    grid_len = len(input_list)

    # 1. & 2. Identify the colored block and the anchor pixel
    block_info = find_colored_block(input_list)
    anchor_index = find_anchor_pixel(input_list)

    # If block or anchor not found, return input unchanged
    if block_info is None or anchor_index is None:
        # print("Warning: Block or anchor not found. Returning original grid.")
        return input_grid # Return original numpy array

    block_start, block_end, block_color = block_info
    block_length = block_end - block_start + 1

    # 3. Calculate the target position for the block
    target_end_index = anchor_index - 1

    # Check if the block is already in the target position
    if block_end == target_end_index:
        return input_grid # Return original numpy array, no shift needed

    # Calculate new start and end indices
    new_block_end = target_end_index
    new_block_start = new_block_end - block_length + 1

    # Check for boundary conditions (shouldn't happen with valid ARC inputs/rules)
    if new_block_start < 0 or new_block_end >= grid_len:
        # print("Warning: Calculated shift results in out-of-bounds position. Returning original grid.")
        return input_grid # Or handle error appropriately

    # 4. & 5. Create the output grid
    # Initialize output with white pixels
    output_list = [WHITE] * grid_len

    # Place the anchor pixel
    output_list[anchor_index] = AZURE

    # Place the shifted block
    for i in range(block_length):
        output_list[new_block_start + i] = block_color

    # Convert back to numpy array with original shape
    output_grid = np.array(output_list).reshape(input_grid.shape)

    return output_grid