```python
import numpy as np
from typing import List, Tuple, Optional

"""
Shift a contiguous block of a non-white (0), non-azure (8) color within a 1D list (row) 
rightward until its rightmost edge is immediately adjacent to the left of the single 
azure (8) pixel. The space previously occupied by the block is filled with white (0). 
Pixels at indices greater than the azure pixel's index remain unchanged.
"""

def find_movable_block(row: np.ndarray) -> Optional[Tuple[int, int, int]]:
    """
    Finds the contiguous block of non-white (0), non-azure (8) color in a 1D row.

    Args:
        row: The 1D input row as a numpy array.

    Returns:
        A tuple containing (color, start_index, end_index) of the block,
        or None if no such block is found.
    """
    start_index = -1
    block_color = -1
    for i, pixel in enumerate(row):
        # Look for a pixel that starts or continues the block
        if pixel != 0 and pixel != 8:
            if start_index == -1:  # Start of a new block
                start_index = i
                block_color = pixel
            # Task examples imply block color is consistent, so we don't strictly need
            # to check pixel == block_color here, just that it's not 0 or 8.
            # If we encounter a different non-0/8 color, it implies end of block based on examples.
            elif pixel != block_color: 
                 return block_color, start_index, i - 1
        # If we were tracking a block and hit background (0) or target (8), the block ends
        elif start_index != -1: 
            return block_color, start_index, i - 1
            
    # Handle case where block goes uninterrupted to the end of the grid
    if start_index != -1:
        return block_color, start_index, len(row) - 1
        
    return None # No block found


def find_target_pixel(row: np.ndarray) -> Optional[int]:
    """
    Finds the index of the single azure (8) pixel in a 1D row.

    Args:
        row: The 1D input row as a numpy array.

    Returns:
        The index of the azure pixel, or None if not found or multiple found. 
        (Examples imply exactly one target).
    """
    indices = np.where(row == 8)[0]
    if len(indices) == 1:
        return indices[0]
    # Handle cases where 0 or >1 targets are found, although examples suggest exactly 1.
    # Returning None signifies an unexpected state based on examples.
    return None 


def transform(input_list: List[int]) -> List[int]:
    """
    Applies the block shifting transformation to the input list.

    Args:
        input_list: A list of integers representing the 1D input row.

    Returns:
        A list of integers representing the transformed 1D output row.
    """
    # --- Input Validation and Setup ---
    if not isinstance(input_list, list) or not input_list:
         # Return input or raise error if input is invalid format
         # Based on expected ARC format, returning input might be safer default
         return input_list 
         # raise ValueError("Input must be a non-empty list.") 

    input_row = np.array(input_list)
    row_len = len(input_row)

    # Initialize output row with background color (white = 0)
    output_row = np.zeros(row_len, dtype=int)

    # --- Find Objects ---
    # Find the movable block details (color, start, end)
    block_info = find_movable_block(input_row)
    if not block_info:
        # If no block found, transformation cannot proceed as defined.
        # Return original list as per observed behavior in similar ARC tasks.
        return input_list 

    block_color, block_start, block_end = block_info
    block_length = block_end - block_start + 1

    # Find the target azure pixel's index
    target_index = find_target_pixel(input_row)
    if target_index is None:
        # If no target pixel, transformation cannot proceed as defined.
        # Return original list.
        return input_list 

    # --- Calculate New Position ---
    # Determine the target end position for the block (adjacent to target)
    new_block_end = target_index - 1
    # Determine the target start position based on end position and block length
    new_block_start = new_block_end - block_length + 1

    # --- Construct Output List ---
    # Check if the calculated position is valid within the list bounds
    if new_block_start < 0:
        # This case implies the block is too long to fit left of the target.
        # Examples don't cover this, returning original seems safest.
        return input_list 
        # Alternatively, one could place a truncated block if rules allowed.
        # print(f"Warning: Calculated block start index {new_block_start} is out of bounds.")

    # Place the block in the output row at the calculated new position
    output_row[new_block_start : new_block_end + 1] = block_color

    # Place the target pixel (8) in the output row at its original index
    # Bounds check target_index, though find_target_pixel should ensure it's valid
    if 0 <= target_index < row_len:
        output_row[target_index] = 8

    # Copy any pixels from the input that were originally to the right of the target pixel
    if target_index + 1 < row_len:
        # Get the segment of the input row after the target pixel
        pixels_to_copy = input_row[target_index + 1:]
        # Determine the corresponding slice in the output row
        output_slice_start = target_index + 1
        output_slice_end = output_slice_start + len(pixels_to_copy)
        # Place the copied pixels into the output row
        output_row[output_slice_start:output_slice_end] = pixels_to_copy

    # Convert the final numpy array back to a list
    return output_row.tolist()
```