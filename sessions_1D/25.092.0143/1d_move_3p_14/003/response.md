```python
"""
Transforms a 1D input grid by shifting a single contiguous block of non-white 
pixels to the right such that exactly one white pixel remains to its right. 
The size of the grid and the color and length of the block are preserved.
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
               otherwise (None, None, None, None).
    """
    non_white_indices = np.where(grid_1d != 0)[0]
    if len(non_white_indices) == 0:
        return None, None, None, None # No non-white pixels found

    start_index = non_white_indices[0]
    color = grid_1d[start_index]
    
    # Find the end of the contiguous block of the *same* color
    end_index = start_index
    for i in range(start_index + 1, len(grid_1d)):
        if grid_1d[i] == color:
            end_index = i
        else:
            break # End of the contiguous block of this color
            
    length = end_index - start_index + 1
         
    return start_index, end_index, color, length

def transform(input_grid):
    """
    Shifts the non-white block in the 1D input grid to the right, 
    leaving exactly one white pixel after it.
    
    Args:
        input_grid (list or numpy array): A 1D list or array representing the input row.
        
    Returns:
        numpy array: The transformed 1D grid.
    """
    # Ensure input is a numpy array for easier manipulation
    input_grid_np = np.array(input_grid)
    grid_length = len(input_grid_np)

    # 1. Identify the single contiguous block of non-white pixels.
    start_index, end_index, block_color, block_length = find_non_white_block(input_grid_np)

    # If no non-white block exists, return the input grid unchanged.
    if start_index is None:
        return input_grid_np 

    # 2. Count the number of white pixels to the right of the block.
    # Indices after the block range from end_index + 1 to grid_length - 1
    # The number of positions is (grid_length - 1) - (end_index + 1) + 1 = grid_length - end_index - 1
    trailing_whites = grid_length - 1 - end_index
    
    # 3. Calculate the required rightward shift amount.
    # We want exactly 1 trailing white pixel.
    # shift_amount = current_trailing_whites - desired_trailing_whites
    shift_amount = trailing_whites - 1
    
    # Handle cases where no shift is needed or possible (e.g., already correct)
    # Based on problem constraints, shift_amount should typically be >= 0
    if shift_amount < 0:
        shift_amount = 0 # Block is already at or past the target position

    # 4. Calculate the new starting index for the block.
    new_start_index = start_index + shift_amount
    
    # Calculate the new end index (inclusive)
    new_end_index = new_start_index + block_length - 1

    # Defensive check: ensure the new block position is within bounds.
    # The requirement of 1 trailing white pixel should inherently guarantee this
    # if the logic is correct and grid_length >= block_length + 1.
    if new_end_index >= grid_length:
         # This scenario implies an issue, perhaps block_length = grid_length?
         # Or shift calculation error under edge conditions.
         # For this problem's examples, it should fit.
         # If it happens, maybe return original? Or raise error?
         # Let's stick to the calculated logic. If it goes out, it's an error state.
         # Re-evaluating: the target state (1 trailing white) means new_end_index = grid_length - 2
         # So this check is primarily for unexpected inputs or logic flaws.
         # Let's assume valid inputs per ARC task structure.
         pass # Proceed based on calculation

    # 5. Create the output grid, initialized with white pixels.
    output_grid = np.zeros_like(input_grid_np)
    
    # 6. Place the non-white block into the output grid at the new position.
    # Ensure slicing handles the case where new_start_index might be out of bounds
    # (though logic should prevent this for valid shifts)
    if new_start_index < grid_length and new_end_index < grid_length:
        output_grid[new_start_index : new_end_index + 1] = block_color
    elif new_start_index < grid_length: # If only start is in bounds (block truncated) - shouldn't happen
         output_grid[new_start_index:] = block_color # Fill till end - adjust length? No, use original block color/length
         # Correction: Use calculated end index clipped to bounds
         actual_end = min(new_end_index, grid_length - 1)
         output_grid[new_start_index : actual_end + 1] = block_color


    # 7. Return the constructed output grid.
    return output_grid
```