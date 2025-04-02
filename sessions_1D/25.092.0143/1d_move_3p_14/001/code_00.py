"""
Transforms a 1D input grid by shifting a contiguous block of non-white pixels 
to the right such that exactly one white pixel remains to its right.

The transformation involves:
1. Identifying the single contiguous block of a non-white color in the input row.
2. Counting the number of white pixels immediately following this block (trailing whites).
3. Calculating the shift distance needed to leave exactly one trailing white pixel (shift = trailing_whites - 1).
4. Constructing the output row by placing the non-white block at its new shifted position, ensuring it's preceded by the appropriate number of leading white pixels and followed by exactly one white pixel. The overall grid size remains the same.
"""

import numpy as np

def find_non_white_block(grid_1d):
    """Finds the start index, end index, color, and length of the non-white block."""
    non_white_indices = np.where(grid_1d != 0)[0]
    if len(non_white_indices) == 0:
        return None, None, None, None # No non-white block found

    start_index = non_white_indices[0]
    end_index = non_white_indices[-1]
    color = grid_1d[start_index]
    length = end_index - start_index + 1
    
    # Verify contiguity (although the problem description implies it)
    if not np.all(grid_1d[start_index : end_index + 1] == color):
         # This case shouldn't happen based on examples, but good for robustness
         raise ValueError("Detected non-contiguous or mixed-color block where one was expected.")
         
    return start_index, end_index, color, length

def count_trailing_whites(grid_1d, block_end_index):
    """Counts the number of white pixels after the block."""
    return np.sum(grid_1d[block_end_index + 1:] == 0)

def transform(input_grid):
    """
    Shifts the non-white block in the input grid to the right, 
    leaving exactly one white pixel after it.
    
    Args:
        input_grid (list or numpy array): A 1D list or array representing the input row.
        
    Returns:
        numpy array: The transformed 1D grid.
    """
    # Ensure input is a numpy array for easier manipulation
    input_grid_np = np.array(input_grid)
    grid_length = len(input_grid_np)

    # 1. Identify the contiguous block of non-white pixels.
    start_index, end_index, block_color, block_length = find_non_white_block(input_grid_np)

    if start_index is None:
        # If there's no block (all white), return the input as is.
        return input_grid_np 

    # 2. Count the number of trailing white pixels.
    trailing_whites = count_trailing_whites(input_grid_np, end_index)
    
    # 3. Calculate the required rightward shift amount.
    # The goal is to have 1 trailing white pixel.
    # Current trailing whites = N
    # Desired trailing whites = 1
    # Change in trailing whites = 1 - N
    # Since moving right decreases trailing whites, shift amount = N - 1
    shift_amount = trailing_whites - 1

    # Ensure shift doesn't push the block out of bounds (shouldn't happen if logic is right)
    if shift_amount < 0:
        # This implies the block is already at or past the target position.
        # Based on examples, this scenario might not occur, but handle defensively.
        print(f"Warning: Calculated negative shift ({shift_amount}). Block might be already positioned correctly or requires left shift (not described). Assuming no shift needed.")
        shift_amount = 0
        
    # 4. Construct the output row.
    # Initialize output grid with white pixels
    output_grid = np.zeros_like(input_grid_np)
    
    # Calculate new position
    new_start_index = start_index + shift_amount
    new_end_index = new_start_index + block_length -1 # End index is inclusive

    # Check bounds for the new position
    if new_end_index >= grid_length:
         raise ValueError("Calculated shift pushes block out of bounds.")

    # Place the block in the new position
    output_grid[new_start_index : new_end_index + 1] = block_color

    return output_grid