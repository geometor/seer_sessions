import numpy as np
from typing import List, Tuple, Optional

"""
Transforms a 1D input grid by reflecting a colored block across a maroon anchor pixel.

The transformation rule involves:
1. Identifying a single maroon (9) pixel (the anchor) and a single contiguous block of another color (non-white, non-maroon).
2. Calculating the distance ('d') between the end index of the colored block and the index of the anchor pixel.
3. Determining the new starting position for the colored block by adding this distance 'd' to the anchor pixel's index.
4. Creating an output grid of the same size, initially all white (0).
5. Placing the anchor pixel at its original position in the output grid.
6. Placing the colored block (with its original color and length) at the newly calculated starting position in the output grid. The original position of the colored block remains white in the output.
"""

def _find_anchor(row: np.ndarray) -> Optional[int]:
    """Finds the index of the maroon (9) pixel."""
    anchor_indices = np.where(row == 9)[0]
    # Expect exactly one anchor
    if len(anchor_indices) == 1:
        return anchor_indices[0]
    return None # Return None if zero or more than one anchor found

def _find_colored_block(row: np.ndarray) -> Optional[Tuple[int, int, int, int]]:
    """
    Finds the first contiguous block of a single color that is not white (0) or maroon (9).
    Returns: Tuple (block_color, block_start_index, block_end_index, block_length) or None if no block found.
    """
    block_color = -1
    block_start_index = -1
    block_end_index = -1
    width = len(row)

    # Find the start and color of the first eligible block
    for i, pixel in enumerate(row):
        if pixel != 0 and pixel != 9:
            block_color = pixel
            block_start_index = i
            break # Found the start of the first block

    # If no block start was found, return None
    if block_start_index == -1:
        return None

    # Find the end of this specific block
    block_end_index = block_start_index
    for i in range(block_start_index + 1, width):
        if row[i] == block_color:
            block_end_index = i
        else:
            # Stop as soon as the color changes or we hit 0 or 9
            break

    # Calculate block length
    block_length = block_end_index - block_start_index + 1

    return block_color, block_start_index, block_end_index, block_length

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the reflection transformation to the input grid.
    """
    # --- Input Validation and Conversion ---
    # Ensure input is not empty and is a list of lists
    if not input_grid or not isinstance(input_grid, list) or not input_grid[0] or not isinstance(input_grid[0], list):
         # Return empty or handle error appropriately if input is invalid
         return [] # Or maybe return input_grid based on ARC evaluation preference

    # Convert the first row (assuming 1D structure based on examples) to a NumPy array
    input_row = np.array(input_grid[0], dtype=int)
    width = len(input_row)

    # --- Find Key Elements ---
    # Find the maroon anchor pixel's index
    anchor_index = _find_anchor(input_row)
    # Find the properties of the colored block
    block_info = _find_colored_block(input_row)

    # If anchor or block is missing, the rule cannot be applied.
    # Return the input grid unchanged as a fallback.
    if anchor_index is None or block_info is None:
        return input_grid

    # Unpack block information
    block_color, block_start_index, block_end_index, block_length = block_info

    # --- Initialize Output Grid ---
    # Create a new row filled with the background color (white, 0)
    output_row = np.zeros_like(input_row)

    # --- Apply Transformation Logic ---
    # Place the anchor pixel in the output grid at its original position
    output_row[anchor_index] = 9

    # Calculate the distance offset: how far the block end is from the anchor
    # This assumes block is always before anchor, as seen in examples
    distance = anchor_index - block_end_index

    # Calculate the new starting index for the block after reflection
    # new_start = anchor + distance
    new_block_start_index = anchor_index + distance

    # Calculate the new ending index for the block
    new_block_end_index = new_block_start_index + block_length - 1

    # --- Populate Output Grid with Transformed Block ---
    # Check if the calculated new block position is valid (within grid bounds)
    if 0 <= new_block_start_index < width and 0 <= new_block_end_index < width:
        # Fill the segment in the output grid with the block's color
        output_row[new_block_start_index : new_block_end_index + 1] = block_color
    else:
        # Optional: Handle cases where the reflected block goes out of bounds.
        # Currently, it just won't be drawn fully or at all if out of bounds.
        # Could add clipping logic if required by task specifics not covered in examples.
        pass

    # --- Format Output ---
    # Convert the resulting NumPy row back to the required list of lists format
    output_grid = [output_row.tolist()]

    return output_grid