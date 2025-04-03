"""
Identify the contiguous horizontal block of pixels whose color is not white (0) 
and not maroon (9). Shift this block exactly 2 positions to the right. 
The space the block vacates becomes white (0). The maroon pixel (9) and 
other white pixels remain in their original positions relative to the grid edges.
"""

import numpy as np

def find_block(grid_row):
    """
    Finds the start index, end index, and color of the non-white, non-maroon block.
    Assumes exactly one such block exists.
    """
    block_start = -1
    block_end = -1
    block_color = -1
    
    for i, pixel in enumerate(grid_row):
        if pixel != 0 and pixel != 9:
            if block_start == -1: # Found the start of the block
                block_start = i
                block_color = pixel
            block_end = i # Keep updating the end as long as we see the color
        elif block_start != -1: # We found the block and now it ended
            break # Stop searching once the block ends
            
    # Handle case where block goes to the end of the grid
    # The loop condition handles this correctly as block_end is updated
            
    if block_start == -1:
        # Should not happen based on task description, but good practice
        return None, None, None 
        
    return block_start, block_end, block_color

def transform(input_grid):
    """
    Transforms the input grid according to the identified rule:
    Shift the non-white, non-maroon block 2 positions to the right.
    """
    # Since the input grids are single rows, work directly with the first row
    # If inputs could be multi-row, we'd need to adapt or check dimensions.
    # For ARC, grids are often numpy arrays, but let's treat it as a list
    # based on the input format shown. Convert to list for easier manipulation if needed.
    
    if isinstance(input_grid, np.ndarray):
        if input_grid.ndim == 2 and input_grid.shape[0] == 1:
             input_row = input_grid[0].tolist()
        elif input_grid.ndim == 1:
             input_row = input_grid.tolist()
        else:
             # Handle unexpected dimensions if necessary
             raise ValueError("Input grid must be 1D or 2D with a single row")
    elif isinstance(input_grid, list):
         # Check if it's a list of lists representing a single row
         if len(input_grid) == 1 and isinstance(input_grid[0], list):
              input_row = input_grid[0]
         # Check if it's already a flat list representing the row
         elif all(isinstance(item, int) for item in input_grid):
              input_row = input_grid
         else:
              raise ValueError("Input grid format not recognized")
    else:
        raise TypeError("Input grid must be a numpy array or a list")

    grid_width = len(input_row)
    
    # Find the block to be moved
    block_start, block_end, block_color = find_block(input_row)

    if block_start is None:
        # If no block found (e.g., all white), return the input as is
        return np.array(input_row).reshape(1, -1) # Return as numpy array (1, N)

    # Initialize the output grid as a copy of the input row
    output_row = list(input_row) # Use list() to ensure it's a mutable copy

    # Define the shift amount
    shift_distance = 2

    # Calculate new block position
    new_block_start = block_start + shift_distance
    new_block_end = block_end + shift_distance

    # Check for boundary conditions (though examples don't hit the edge)
    if new_block_end >= grid_width:
        # This case isn't shown in examples, behaviour is undefined.
        # Option 1: Truncate the block? Option 2: Error? Option 3: Wrap around?
        # Based on ARC principles, truncation or stopping at boundary seems most likely.
        # Let's assume it stops/truncates if it hits the boundary for now.
        # However, the examples provided don't test this. Sticking to the observed pattern.
        # If the task demands boundary handling, it needs clarification.
        # For now, proceed assuming it fits.
        pass # No specific handling needed based *only* on provided examples


    # Clear the original block location in the output grid
    for i in range(block_start, block_end + 1):
        # Check bounds just in case, although logic should be sound
        if 0 <= i < grid_width:
             output_row[i] = 0 # Set to white

    # Draw the block in the new location in the output grid
    for i in range(new_block_start, new_block_end + 1):
         # Ensure we don't write past the grid boundary
         if 0 <= i < grid_width:
              output_row[i] = block_color

    # Return the modified row as a numpy array (standard ARC format)
    # Ensure it's shaped as (1, N)
    return np.array(output_row).reshape(1, -1)
