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
            
    # Calculate the length of the block (inclusive indices)
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

    # 1. Identify the single contiguous block of non-white pixels.
    #    Determine its color, starting index, and length.
    start_index, end_index, block_color, block_length = find_non_white_block(input_grid_np)

    # If no block is found (e.g., all white grid), return the input as is
    if start_index is None:
        return input_grid_np 

    # 2. Create a new output row of the same length as the input row, 
    #    initially filled entirely with white pixels (0).
    output_grid = np.zeros_like(input_grid_np)
    
    # 3. Define the constant shift amount.
    shift_amount = 3
    
    # 4. Calculate the target starting index for the block in the output row 
    #    by adding exactly 3 to the block's starting index from the input row.
    new_start_index = start_index + shift_amount
    # Calculate the corresponding end index (inclusive)
    new_end_index = new_start_index + block_length - 1 

    # 5. Copy the identified non-white block (preserving its color and length) 
    #    into the output row, starting at the calculated target starting index.
    #    Check bounds to prevent errors, although based on examples, it should fit.
    if new_start_index < grid_length and new_end_index < grid_length:
        # Use slice assignment: output[start:end+1] = value
        output_grid[new_start_index : new_end_index + 1] = block_color
    elif new_start_index < grid_length: 
        # Handle partial block placement if it goes off the edge 
        # (not expected for this task based on examples)
         actual_end = grid_length - 1
         output_grid[new_start_index : actual_end + 1] = block_color


    # 6. The resulting output row is the final transformation.
    return output_grid