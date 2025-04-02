import numpy as np
from typing import List

def find_first_color_block_end(row: np.ndarray) -> tuple[int, int]:
    """
    Finds the color and the index of the last pixel of the first contiguous 
    block of non-white (non-zero) color in the row.

    Args:
        row: A 1D numpy array representing the row of pixels.

    Returns:
        A tuple containing:
        - The color of the block (int).
        - The index of the last pixel of the block (int).
        Returns (-1, -1) if no non-white block is found.
    """
    block_color = -1
    block_end_index = -1
    in_block = False
    for i, pixel in enumerate(row):
        if pixel != 0 and not in_block: # Found the start of the first block
            block_color = pixel
            in_block = True
            block_end_index = i # Initialize end index
        elif in_block and pixel == block_color: # Continuing the block
            block_end_index = i # Update end index
        elif in_block and pixel != block_color: # Found the end of the block (different color or white)
            return block_color, block_end_index
        # Need to handle the case where the block goes to the end of the row
    
    # If loop completes and we were in a block, return the last found index
    if in_block:
        return block_color, block_end_index
        
    return -1, -1 # No block found

def find_marker(row: np.ndarray, marker_color: int = 6) -> int:
    """
    Finds the index of the first occurrence of the marker pixel color.

    Args:
        row: A 1D numpy array representing the row of pixels.
        marker_color: The integer value of the color to find (default is 6 for magenta).

    Returns:
        The index of the marker pixel, or -1 if not found.
    """
    try:
        # Convert numpy array to list to use the index method
        return list(row).index(marker_color)
    except ValueError:
        return -1 # Marker not found

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Identifies the first contiguous block of non-white color and a magenta marker pixel 
    in a single row input grid. It then fills the white (0) pixels located strictly 
    between the end of the color block and the magenta marker pixel with the color 
    of the block.
    """
    # The task deals with single-row grids.
    if not input_grid or len(input_grid) != 1:
        # Handle unexpected input format if necessary, though ARC guarantees structure.
        return input_grid 

    # Convert the input row to a numpy array for easier processing
    input_row = np.array(input_grid[0], dtype=int)
    # Create a copy to modify, preserving the original input
    output_row = input_row.copy()

    # 1. Identify the color and end index of the first non-white block
    fill_color, block_end_index = find_first_color_block_end(input_row)

    # 2. Identify the index of the magenta (6) marker pixel
    marker_index = find_marker(input_row, 6)

    # 3. Check if both a block and a marker were found, and the marker is positioned
    #    after the block with at least one pixel potentially in between.
    if fill_color != -1 and marker_index != -1 and marker_index > block_end_index + 1:
        
        # 4. Iterate through the indices strictly between the block's end and the marker's position.
        # The range starts one pixel after the block ends and ends one pixel before the marker.
        fill_start_index = block_end_index + 1
        fill_end_index = marker_index # range() is exclusive of the end index

        for i in range(fill_start_index, fill_end_index):
            # 5. If the pixel at the current index in the *original* row is white (0),
            #    change the corresponding pixel in the *output* row to the fill_color.
            if input_row[i] == 0:
                 output_row[i] = fill_color

    # Return the modified row, formatted back into the required 2D list-of-lists structure
    return [output_row.tolist()]