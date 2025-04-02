"""
Identifies the single contiguous block of non-white pixels in a 1D input grid 
and shifts this block exactly 3 positions to the right to produce the output grid. 
The grid size, block color, and block length remain unchanged. Background pixels 
are white (0).
"""

import numpy as np

def find_non_white_block(grid_1d):
    """
    Finds the start index, end index, color, and length of the first 
    contiguous non-white block found in a 1D grid.

    Args:
        grid_1d (np.array): A 1D numpy array representing the grid row.

    Returns:
        tuple: (start_index, end_index, color, length) if a block is found,
               otherwise (None, None, None, None). Returns indices inclusive.
    """
    # Find indices of all non-white pixels
    non_white_indices = np.where(grid_1d != 0)[0]
    
    # If no non-white pixels, return None for all properties
    if len(non_white_indices) == 0:
        return None, None, None, None 

    # The start index is the first non-white index found
    start_index = non_white_indices[0]
    # The color is the color of the pixel at the start index
    color = grid_1d[start_index]
    
    # Determine the end index of the contiguous block of the *same* color
    end_index = start_index
    # Iterate from the pixel after the start index
    for i in range(start_index + 1, len(grid_1d)):
        # If the pixel matches the block color, update the end index
        if grid_1d[i] == color:
            end_index = i
        # If the pixel is different (white or another color), the block ends
        else:
            break 
            
    # Calculate the length of the block
    length = end_index - start_index + 1
         
    return start_index, end_index, color, length

def transform(input_grid):
    """
    Shifts the non-white block in the 1D input grid 3 positions to the right.
    
    Args:
        input_grid (list or numpy array): A 1D list or array representing the input row.
        
    Returns:
        numpy array: The transformed 1D grid.
    """
    # Ensure input is a numpy array for efficient operations
    input_grid_np = np.array(input_grid)
    grid_length = len(input_grid_np)

    # 1. Find the non-white block in the input grid
    start_index, end_index, block_color, block_length = find_non_white_block(input_grid_np)

    # If no block is found (e.g., all white grid), return the input as is
    if start_index is None:
        return input_grid_np 

    # 2. Initialize the output grid with the same size, filled with white (0)
    output_grid = np.zeros_like(input_grid_np)
    
    # 3. Define the constant shift amount
    shift_amount = 3
    
    # 4. Calculate the new start and end indices for the shifted block
    new_start_index = start_index + shift_amount
    # End index is inclusive, so new end = new start + length - 1
    new_end_index = new_start_index + block_length - 1 

    # 5. Place the block into the output grid at the new position
    # Add checks to prevent writing outside the grid boundaries, though based on
    # examples, the shifted block should always fit.
    if new_start_index < grid_length and new_end_index < grid_length:
        # Slice the output grid and assign the block color
        output_grid[new_start_index : new_end_index + 1] = block_color
    # Handle potential edge cases if shift pushes block partially/fully off grid
    # (Not expected based on training data, but good practice)
    elif new_start_index < grid_length: 
        # If only the start fits, place the truncated part of the block
         output_grid[new_start_index:] = block_color 
         # Note: This assumes partial placement is desired if it overflows.
         # The task examples suggest overflow won't happen.

    # 6. Return the transformed grid
    return output_grid