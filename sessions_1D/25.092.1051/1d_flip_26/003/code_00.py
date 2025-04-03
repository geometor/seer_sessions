import numpy as np
from typing import List, Tuple

"""
Transforms a 1xN input grid by identifying a specific pattern: a single 'marker' 
pixel (the first non-background pixel) followed immediately by a contiguous 'block' 
of pixels of a single, different, non-background color. If this pattern is found, 
the marker pixel is moved to the position immediately following the block, and the 
block pixels are shifted one position to the left to occupy the original marker 
position and the subsequent block positions minus one. If the pattern is not found, 
the grid is returned unchanged.
"""

def find_marker_and_block(row: List[int]) -> Tuple[int, int, int, int, int]:
    """
    Finds the marker pixel and the subsequent block in a row.

    Args:
        row: A list of integers representing a row of the grid.

    Returns:
        A tuple containing:
        - marker_idx: The index of the marker pixel.
        - marker_color: The color of the marker pixel.
        - block_start_idx: The starting index of the block.
        - block_color: The color of the block pixels.
        - block_length: The number of pixels in the block.
        Returns (-1, -1, -1, -1, -1) if no valid marker/block pattern is found.
    """
    marker_idx = -1
    marker_color = -1
    block_start_idx = -1
    block_color = -1
    block_length = 0
    n = len(row)

    # 1. Scan for the first non-background pixel (marker)
    for i, pixel in enumerate(row):
        if pixel != 0:
            marker_idx = i
            marker_color = pixel
            break

    # If no non-background pixel found, the pattern doesn't exist
    if marker_idx == -1:
        return -1, -1, -1, -1, -1

    # 2. Check if there's a pixel immediately following the marker
    if marker_idx + 1 >= n:
        # Marker is at the very end, no block possible
        return -1, -1, -1, -1, -1 

    # 3. Identify the potential start of the block
    block_start_idx = marker_idx + 1
    potential_block_color = row[block_start_idx]

    # 4. Validate the block color (must be non-background and different from marker)
    if potential_block_color == marker_color or potential_block_color == 0:
        # Not a valid block according to the pattern definition
        return -1, -1, -1, -1, -1 
    
    block_color = potential_block_color

    # 5. Calculate block length
    block_length = 0
    for i in range(block_start_idx, n):
        if row[i] == block_color:
            block_length += 1
        else:
            # Block ends when color changes or row ends
            break 

    # 6. Check if a block of at least length 1 was actually found
    if block_length == 0:
         # Should technically be caught by step 4, but good to be explicit
        return -1, -1, -1, -1, -1

    # 7. Final check: Ensure the move is within bounds (optional but safe)
    target_marker_idx = marker_idx + block_length
    if target_marker_idx >= n:
         # The marker would be moved out of bounds
         # This might indicate an edge case not fully covered or an unexpected input
         print(f"Warning: Calculated target marker index {target_marker_idx} is out of bounds for row length {n}.")
         return -1, -1, -1, -1, -1 # Treat as pattern not applicable if move is invalid

    return marker_idx, marker_color, block_start_idx, block_color, block_length


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the marker/block rearrangement transformation to the input grid.
    """
    # Expecting a 1xN grid, represented as [[...]]
    if not input_grid or not input_grid[0]:
        return input_grid # Handle empty or invalid input

    input_row = input_grid[0]
    
    # Create a mutable copy of the row to modify
    output_row = list(input_row) 

    # Find the marker and block details using the helper function
    marker_idx, marker_color, _, block_color, block_length = find_marker_and_block(input_row)

    # Check if the specific marker/block pattern was found
    if marker_idx != -1:
        # If the pattern is found, perform the rearrangement
        
        # Calculate the target index for the marker pixel
        target_marker_idx = marker_idx + block_length

        # Shift the block pixels one step to the left
        # Fill indices from marker_idx up to (but not including) target_marker_idx with block_color
        for i in range(block_length):
            current_idx = marker_idx + i
            # Basic bounds check within the loop (though find_marker_and_block should prevent out-of-bounds)
            if current_idx < len(output_row):
                 output_row[current_idx] = block_color
            else:
                 # This indicates an issue, potentially stop or log
                 print(f"Error: Index {current_idx} out of bounds during block shift.")
                 return input_grid # Return original on error

        # Place the marker pixel at its new position (after the original block)
        # Basic bounds check (find_marker_and_block already performed one)
        if target_marker_idx < len(output_row):
            output_row[target_marker_idx] = marker_color
        else:
             # This indicates an issue, potentially stop or log
             print(f"Error: Target marker index {target_marker_idx} out of bounds during marker placement.")
             return input_grid # Return original on error

    # If the pattern was not found (marker_idx == -1), output_row remains a copy of input_row

    # Return the (potentially modified) row, wrapped in a list to match the 1xN grid format
    return [output_row]