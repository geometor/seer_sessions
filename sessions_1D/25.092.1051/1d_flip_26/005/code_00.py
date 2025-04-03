import numpy as np
from typing import Tuple

"""
Transforms a 1xN input grid (represented as a 2D NumPy array) by identifying a 
specific pattern: the first non-background pixel ('marker') followed immediately 
by a contiguous 'block' of pixels of a single, different, non-background color. 
If this pattern is found, the marker pixel is moved to the position immediately 
following the block's original end position, and the block pixels are shifted 
one position to the left to occupy the original marker position and the subsequent 
block positions minus one. If the pattern is not found or the move is invalid 
(e.g., goes out of bounds), the original grid is returned unchanged.
"""

def find_marker_and_block_np(row: np.ndarray) -> Tuple[int, int, int, int]:
    """
    Finds the marker pixel and the subsequent block in a 1D NumPy array row.

    Args:
        row: A 1D NumPy array representing a row of the grid.

    Returns:
        A tuple containing:
        - marker_idx: The index of the marker pixel.
        - marker_color: The color of the marker pixel.
        - block_color: The color of the block pixels.
        - block_length: The number of pixels in the block.
        Returns (-1, -1, -1, -1) if no valid marker/block pattern is found
        or if the required rearrangement would go out of bounds.
    """
    n = row.shape[0]
    marker_idx = -1
    marker_color = -1
    block_color = -1
    block_length = 0

    # 1. Find the index of the first non-background pixel (marker)
    non_background_indices = np.where(row != 0)[0]
    if non_background_indices.size == 0:
        return -1, -1, -1, -1 # No non-background pixels found
    
    marker_idx = non_background_indices[0]
    marker_color = row[marker_idx]

    # 2. Check if there's a pixel immediately following the marker
    if marker_idx + 1 >= n:
        return -1, -1, -1, -1 # Marker is at the end, no block possible

    # 3. Identify the potential block color
    potential_block_color = row[marker_idx + 1]

    # 4. Validate the block color (must be non-background and different from marker)
    if potential_block_color == 0 or potential_block_color == marker_color:
        return -1, -1, -1, -1 # Invalid block color

    block_color = potential_block_color

    # 5. Calculate block length
    block_start_idx = marker_idx + 1
    for i in range(block_start_idx, n):
        if row[i] == block_color:
            block_length += 1
        else:
            break # Block ends

    # 6. Check if a block was actually found (length >= 1)
    if block_length == 0:
         # This case should be covered by step 4, but double-check
        return -1, -1, -1, -1

    # 7. Check if the target position for the marker is within bounds
    target_marker_idx = marker_idx + block_length
    if target_marker_idx >= n:
        # The move would place the marker out of bounds
        return -1, -1, -1, -1

    return marker_idx, marker_color, block_color, block_length


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the marker/block rearrangement transformation to the input grid.
    """
    # Validate input shape (must be 1xN)
    if input_grid.ndim != 2 or input_grid.shape[0] != 1:
        # Or handle potential multiple rows if the task definition evolves
        # For now, assume strictly 1xN based on examples
        print("Warning: Input grid is not 1xN. Returning original grid.")
        return input_grid
        
    # Extract the row (it's a view, so copy it for modification)
    input_row = input_grid[0]
    output_row = np.copy(input_row)
    
    # Find the marker and block details
    marker_idx, marker_color, block_color, block_length = find_marker_and_block_np(output_row)

    # Check if the specific marker/block pattern was found and is valid
    if marker_idx != -1:
        # Pattern found, perform the rearrangement
        
        # Calculate the target index for the marker pixel
        target_marker_idx = marker_idx + block_length # Already bounds-checked in helper

        # Shift the block pixels one step to the left using slicing
        # Overwrite pixels from marker_idx up to (but not including) target_marker_idx
        output_row[marker_idx:target_marker_idx] = block_color
        
        # Place the marker pixel at its new position
        output_row[target_marker_idx] = marker_color
        
        # Reshape the modified 1D row back into a 2D (1, N) array
        return output_row.reshape(1, -1)
        
    else:
        # Pattern not found or invalid, return the original grid
        return input_grid