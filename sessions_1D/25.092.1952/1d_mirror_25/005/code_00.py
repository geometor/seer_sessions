import numpy as np
from typing import List, Tuple, Optional

"""
Transforms a 1D input grid by reflecting a colored block across a maroon anchor pixel.

1.  Receives the input grid (expected as `List[List[int]]`). Extracts the first row for processing and converts it into a NumPy array.
2.  Initializes an output NumPy array of the same width, filled with white (0).
3.  Finds the index (`anchor_index`) of the single maroon (9) pixel in the input row. If not found, returns the input grid.
4.  Places the maroon (9) pixel at `anchor_index` in the output array.
5.  Finds the single contiguous block of non-white, non-maroon pixels in the input row. Identifies its color (`block_color`), start index (`block_start_index`), end index (`block_end_index`), and length (`block_length`). If not found, returns the input grid.
6.  Calculates the distance (`d`) between the end of the input block and the anchor pixel: `d = anchor_index - block_end_index`. Assumes the block is always before the anchor.
7.  Calculates the new starting index (`new_block_start_index`) for the colored block in the output array: `new_block_start_index = anchor_index + d`.
8.  Calculates the new ending index (`new_block_end_index`).
9.  Checks if the new block position is within bounds.
10. If within bounds, fills the corresponding pixels in the output array with the `block_color`.
11. Converts the final output NumPy array back into the `List[List[int]]` format and returns it.
"""


def _find_anchor(row: np.ndarray) -> Optional[int]:
    """Finds the index of the single maroon (9) pixel."""
    anchor_indices = np.where(row == 9)[0]
    # Expect exactly one anchor
    if len(anchor_indices) == 1:
        # Use .item() to convert numpy int to standard python int
        return anchor_indices[0].item()
    return None # Return None if zero or more than one anchor found

def _find_colored_block(row: np.ndarray) -> Optional[Tuple[int, int, int, int]]:
    """
    Finds the single contiguous block of a color that is not white (0) or maroon (9).
    Returns: Tuple (block_color, block_start_index, block_end_index, block_length) or None if no single valid block found.
    """
    block_color = -1
    block_start_index = -1
    block_end_index = -1
    width = len(row)
    found_block = False

    for i, pixel in enumerate(row):
        # Look for the start of a potential block
        if pixel != 0 and pixel != 9:
            # Found a non-white, non-maroon pixel
            if not found_block:
                # This is the start of the first potential block
                block_color = pixel.item() # Store color
                block_start_index = i
                block_end_index = i # Assume length 1 initially
                found_block = True
            elif pixel == block_color:
                 # Continue the current block
                 block_end_index = i
            else:
                 # Found a different color - indicates more than one block or noise
                 return None # Problem statement implies only one block
        elif found_block:
            # We were in a block, but now hit 0 or 9, so the block ends here.
            break # Exit loop once the block ends

    # Check if a valid block was found
    if found_block:
        block_length = block_end_index - block_start_index + 1
        # Verify only one block: Scan the rest of the array for other colored pixels
        for i in range(block_end_index + 1, width):
             if row[i] != 0 and row[i] != 9:
                 return None # Found another colored pixel after the block ended
        return block_color, block_start_index, block_end_index, block_length
    else:
        # No block start was ever found
        return None


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the reflection transformation to the input grid.
    """
    # --- Input Validation and Conversion ---
    # Check if input_grid is a list and contains at least one row (list)
    if not isinstance(input_grid, list) or len(input_grid) == 0 or not isinstance(input_grid[0], list):
         # Invalid format, return input or appropriate error indication
         # Returning input is often preferred in ARC if rules don't match
         return input_grid
    if len(input_grid[0]) == 0: # Handle empty row case
        return input_grid

    # Convert the first row to a NumPy array for efficient processing
    try:
        input_row = np.array(input_grid[0], dtype=int)
    except ValueError:
         # Handle case where row contains non-integer elements if necessary
         return input_grid # Return input if conversion fails
         
    width = len(input_row)

    # --- Find Key Elements ---
    # Find the maroon anchor pixel's index
    anchor_index = _find_anchor(input_row)
    # Find the properties of the colored block
    block_info = _find_colored_block(input_row)

    # --- Pre-computation Checks ---
    # If anchor or block is missing or invalid (e.g., multiple blocks),
    # the specific transformation rule cannot be applied. Return input grid.
    if anchor_index is None or block_info is None:
        return input_grid

    # Unpack block information (already standard Python types from helpers)
    block_color, block_start_index, block_end_index, block_length = block_info

    # --- Initialize Output Grid ---
    # Create a new row filled with the background color (white, 0)
    output_row = np.zeros_like(input_row) # Creates numpy array of same shape/type

    # --- Apply Transformation Logic ---
    # Place the anchor pixel in the output grid at its original position
    # Ensure anchor_index is within bounds (should be if found correctly)
    if 0 <= anchor_index < width:
        output_row[anchor_index] = 9
    else:
         # This case should ideally not happen if _find_anchor works
         return input_grid # Safety return

    # Calculate the distance offset: how far the block end is from the anchor
    # Assumes block is always before anchor, as seen in examples
    distance = anchor_index - block_end_index

    # Calculate the new starting index for the block after reflection
    new_block_start_index = anchor_index + distance

    # Calculate the new ending index for the block
    new_block_end_index = new_block_start_index + block_length - 1

    # --- Populate Output Grid with Transformed Block ---
    # Check if the calculated new block position is valid (within grid bounds)
    # Important: Slicing end index is exclusive, so use new_block_end_index + 1
    if 0 <= new_block_start_index < width and 0 <= new_block_end_index < width:
        # Fill the segment in the output grid with the block's color
        output_row[new_block_start_index : new_block_end_index + 1] = block_color
    # Else: If the block goes out of bounds, it's simply not drawn there.
    # The output_row already has 0s in those positions.

    # --- Format Output ---
    # Convert the resulting NumPy row back to the required List[List[int]] format
    # Need [[val1, val2, ...]]
    output_grid = [output_row.tolist()]

    return output_grid