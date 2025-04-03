"""
Identifies a contiguous block of non-white pixels in each row of a 2D input grid, 
shifts this block one position to the right within its row, sets the original 
starting position of the block to white (0), and sets the position immediately 
to the right of the original block's end to the block's color. If a row contains 
no non-white block, or the block is at the rightmost edge, the row remains unchanged 
(except potentially the start pixel becoming white if it's at the edge).
"""

import numpy as np

def find_non_white_block_in_row(row):
    """
    Finds the start index, end index, and color of the first contiguous 
    block of non-white pixels in a 1D array (row).
    
    Args:
        row (np.ndarray): The input 1D array representing a row.
        
    Returns:
        tuple: (start_index, end_index, block_color) or (None, None, None) 
               if no non-white block is found.
    """
    start_index = -1
    end_index = -1
    block_color = 0
    
    for i, pixel in enumerate(row):
        if pixel != 0: # Found a non-white pixel
            if start_index == -1: # Start of a potential block
                start_index = i
                block_color = pixel
            end_index = i # Update end index as long as we see non-white
        elif start_index != -1: # Found the first white pixel after the block started
            # Verify the block found so far is single-colored
            if not np.all(row[start_index : end_index + 1] == block_color):
                 # If multi-colored, reset and continue search (or handle error)
                 # Based on examples, blocks are single-colored. Let's assume this holds.
                 # If needed, add error handling or logic to find the *correct* block.
                 # For now, we break assuming the first contiguous non-white segment is the target.
                 pass # Or handle error if strict single-color block is required
            
            break # Block ended, stop searching in this row
            
    if start_index == -1:
        return None, None, None # No block found in the row
        
    # Final check if block ended at the edge of the row
    if start_index != -1:
         if not np.all(row[start_index : end_index + 1] == block_color):
             # Handle potential multi-color issue if block ends at row edge
             # For simplicity, we'll trust the first color found
             pass

    return start_index, end_index, block_color

def process_row(row):
    """
    Applies the shift transformation to a single row if applicable.
    
    Args:
        row (np.ndarray): The input 1D array representing a row.
        
    Returns:
        np.ndarray: The transformed row.
    """
    # Find the non-white block in the row
    start_index, end_index, block_color = find_non_white_block_in_row(row)
    
    # Make a copy to modify
    output_row = row.copy()
    row_length = len(row)

    # If a block was found, perform the shift logic
    if start_index is not None:
        # Check if there's space to shift right (index exists and is white)
        if end_index + 1 < row_length and output_row[end_index + 1] == 0:
            # Set the original start position to white (background)
            output_row[start_index] = 0
            
            # Set the position after the original end to the block's color
            output_row[end_index + 1] = block_color
        # Handle edge case: block is at the very end or blocked
        elif end_index + 1 >= row_length: 
            # Block cannot shift right as it's at the edge. 
            # Based on task description, only the start pixel changes.
             output_row[start_index] = 0
             # Potentially print a warning or log this edge case if needed.
             # print(f"Warning: Block ending at index {end_index} cannot shift right in row.")
        else: 
             # Block is blocked by another non-white pixel. 
             # Similar to edge case, change start pixel only.
             output_row[start_index] = 0
             # Potentially print a warning or log this edge case if needed.
             # print(f"Warning: Block ending at index {end_index} is blocked from shifting right in row.")


    # Return the modified (or original if no block found) row
    return output_row


def transform(input_grid):
    """
    Transforms the input grid by shifting the contiguous non-white block 
    in each row one step to the right, where possible.

    Args:
        input_grid (np.ndarray): A 2D NumPy array representing the input grid.

    Returns:
        np.ndarray: A new 2D NumPy array representing the transformed grid.
    """
    # Ensure input is a numpy array
    if not isinstance(input_grid, np.ndarray):
        input_grid = np.array(input_grid)
        
    # Initialize output_grid with the same shape and type as input
    output_grid = np.copy(input_grid)
    
    # Iterate through each row of the grid
    for r in range(input_grid.shape[0]):
        # Process the current row
        transformed_row = process_row(input_grid[r])
        # Update the corresponding row in the output grid
        output_grid[r] = transformed_row
        
    return output_grid