"""
Processes a grid by examining each row independently. 
If a row contains exactly two non-white pixels, the color of the rightmost pixel 
is copied to the cell immediately to the right of the leftmost pixel, and the 
original position of the rightmost pixel is set to white (0). 
Rows with zero, one, or more than two non-white pixels remain unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list): A list of lists representing the input grid.

    Returns:
        list: A list of lists representing the transformed output grid.
    """
    # Convert the input list of lists to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    # Create a copy of the input grid to modify, which will become the output grid
    output_np = np.copy(input_np)
    
    # Get the dimensions of the grid
    height, width = input_np.shape

    # Iterate through each row of the grid
    for r in range(height):
        # Find the column indices of all non-white (non-zero) pixels in the current row
        non_white_cols = np.where(input_np[r, :] != 0)[0]
        
        # Check if there are exactly two non-white pixels in this row
        if len(non_white_cols) == 2:
            # Identify the column index of the leftmost non-white pixel
            col_left = non_white_cols[0]
            # Identify the column index of the rightmost non-white pixel
            col_right = non_white_cols[1]
            
            # Get the color of the rightmost non-white pixel
            color_right = input_np[r, col_right]
            
            # Calculate the target column index, immediately to the right of the leftmost pixel
            target_col = col_left + 1
            
            # Ensure the target column is within the grid bounds (although examples imply it's safe)
            # And also ensure we are not trying to write past the original rightmost pixel's position
            # based on observed behavior (target col < col_right)
            if target_col < width and target_col < col_right:
                 # Copy the color of the rightmost pixel to the target position in the output grid
                 output_np[r, target_col] = color_right
                 
                 # Set the original position of the rightmost pixel to white (0) in the output grid
                 output_np[r, col_right] = 0
            # Handle the edge case where the two pixels are adjacent (target_col == col_right)
            elif target_col == col_right:
                 # In this specific case, the right pixel effectively overwrites itself (no visual change)
                 # but its original position still needs to be cleared according to the rule.
                 # However, the examples suggest this doesn't happen, the rule implies movement *into* a space.
                 # Let's stick to the observed pattern: if target_col >= col_right, perhaps nothing happens?
                 # Re-evaluating: The rule is "move right pixel's color next to left, clear right pixel".
                 # If they are adjacent, left+1 *is* the right pixel's column.
                 # So, output_np[r, col_right] = color_right (redundant)
                 # and output_np[r, col_right] = 0. Clearing takes precedence.
                 output_np[r, col_right] = 0 # Clear original right pixel position
                 # No color needs to be explicitly copied as it would be immediately cleared.


            # If target_col > col_right, this contradicts the problem structure seen so far.
            # The code currently does nothing in this unlikely scenario.


    # Convert the final numpy array back to a list of lists before returning
    return output_np.tolist()
