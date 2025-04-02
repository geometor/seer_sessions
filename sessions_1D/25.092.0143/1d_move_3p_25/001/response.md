```python
import numpy as np

"""
This module transforms an input grid (represented as a 1D numpy array) by 
identifying a single contiguous block of non-white (non-zero) pixels and 
shifting this block 3 positions to the right. The space vacated by the 
block is filled with the background color (white, 0). The color and 
length of the block are preserved.
"""

def find_colored_block(grid_1d):
    """
    Finds the first contiguous block of non-zero pixels in a 1D numpy array.

    Args:
        grid_1d: A 1D numpy array representing a row of pixels.

    Returns:
        A tuple (color, start_index, length) if a block is found,
        otherwise None. Returns None if no non-zero pixels are found.
    """
    non_zero_indices = np.where(grid_1d != 0)[0]
    if len(non_zero_indices) == 0:
        return None  # No colored block found

    start_index = non_zero_indices[0]
    color = grid_1d[start_index]
    
    # Find the end of the contiguous block
    length = 0
    for i in range(start_index, len(grid_1d)):
        if grid_1d[i] == color:
            length += 1
        else:
            break
            
    # Verify contiguity (optional but good practice)
    # expected_indices = np.arange(start_index, start_index + length)
    # if not np.array_equal(non_zero_indices[:length], expected_indices):
    #     # This handles cases with multiple blocks or gaps, though not expected by the prompt
    #     print("Warning: Non-contiguous block detected or multiple blocks found. Using the first part.")
        
    return color, start_index, length

def transform(input_grid):
    """
    Shifts the single colored block in the input grid 3 positions to the right.

    Args:
        input_grid: A list or 1D numpy array representing the input row.

    Returns:
        A 1D numpy array representing the transformed output row.
    """
    # Ensure input is a numpy array
    input_array = np.array(input_grid)
    
    # Define background color
    background_color = 0
    
    # Get grid dimensions
    grid_length = len(input_array)
    
    # Initialize output grid with background color
    output_grid = np.full(grid_length, background_color, dtype=input_array.dtype)
    
    # Find the colored block in the input
    block_info = find_colored_block(input_array)
    
    if block_info:
        color, start_index, length = block_info
        
        # Calculate the new starting position
        new_start_index = start_index + 3
        
        # Calculate the new ending position (exclusive)
        new_end_index = new_start_index + length
        
        # Ensure the new position is within bounds (clip if necessary, though examples suggest it fits)
        # Adjust indices if they go out of bounds
        actual_start = max(0, new_start_index)
        actual_end = min(grid_length, new_end_index)
        
        # Calculate the length to actually draw (in case of clipping)
        draw_length = actual_end - actual_start
        
        # Place the block in the output grid at the new position
        if draw_length > 0 :
             # Determine which part of the original block to draw if clipped at start
            block_offset = max(0, -new_start_index) 
            output_grid[actual_start:actual_end] = color # Fill with the block's color

    # Return the modified grid
    return output_grid.tolist() # Return as list to match expected output format if needed, or keep as array

```