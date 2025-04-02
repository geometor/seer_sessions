import numpy as np
import math

"""
Identify the contiguous block of non-white pixels in the input row. Determine its color, length (L), and starting column index (S_in). Calculate the new starting column index (S_out) by adding the length (L) to the input starting index (S_in): S_out = S_in + L. Create a new output row of the same length, initially filled with white pixels (0). Place the identified block (using its original color and length L) into the output row starting at the calculated index S_out.
"""

def find_non_white_block(grid_row):
    """Finds the first contiguous non-white block in a 1D array."""
    non_white_indices = np.where(grid_row != 0)[0]
    if len(non_white_indices) == 0:
        return None, -1, -1  # No block found

    start_index = non_white_indices[0]
    color = grid_row[start_index]
    length = 0
    for i in range(start_index, len(grid_row)):
        if grid_row[i] == color:
            length += 1
        else:
            break
            
    # Verify contiguity (although simple cases make this less critical)
    expected_indices = np.arange(start_index, start_index + length)
    if not np.array_equal(non_white_indices[:length], expected_indices):
         # This handles cases where there might be multiple blocks, 
         # but the prompt implies only one. We focus on the first one found.
         pass # For this specific task structure, the first block is sufficient.

    return color, start_index, length

def transform(input_grid):
    """
    Shifts a contiguous block of non-white pixels to the right by its own length.
    
    Args:
        input_grid (np.array): A 1D numpy array representing the input row.

    Returns:
        np.array: A 1D numpy array representing the transformed output row.
    """
    # Ensure input is a NumPy array
    if not isinstance(input_grid, np.ndarray):
      input_grid = np.array(input_grid, dtype=int)

    # Assuming the input is always 1D based on examples
    if input_grid.ndim > 1:
         # Handle potential 2D array with single row
         if input_grid.shape[0] == 1:
             input_row = input_grid[0]
         else:
             raise ValueError("Input grid must be 1-dimensional or a single row.")
    else:
        input_row = input_grid

    grid_width = len(input_row)

    # Initialize output_grid with white pixels (0)
    output_grid = np.zeros_like(input_row)

    # 1. Identify the non-white block, its color, length (L), and start index (S_in)
    color, start_index, length = find_non_white_block(input_row)

    # If no block is found, return the all-white grid (although examples imply a block exists)
    if color is None:
        return output_grid.reshape(input_grid.shape) # return in original shape

    # 2. Calculate the new starting index (S_out)
    new_start_index = start_index + length

    # 3. Calculate the end index for placing the block
    new_end_index = new_start_index + length

    # 4. Place the block in the output grid, ensuring it fits within bounds
    if new_start_index < grid_width:
        # Determine the actual end index, clipping if necessary
        actual_end_index = min(new_end_index, grid_width)
        # Determine the length of the block to actually place (might be clipped)
        place_length = actual_end_index - new_start_index
        
        # Place the colored block
        output_grid[new_start_index:actual_end_index] = color

    # Reshape the output to match the original input shape (e.g., [[...]] vs [...])
    return output_grid.reshape(input_grid.shape)
