"""
Processes a grid by examining each row independently. 
If a row contains exactly two non-white pixels, and the colors of these two pixels 
(leftmost, rightmost) form one of the specific pairs (Blue=1, Azure=8), 
(Azure=8, Blue=1), (Yellow=4, Orange=7), or (Orange=7, Yellow=4), then the 
color of the rightmost pixel is copied to the cell immediately to the right of the 
leftmost pixel, and the original position of the rightmost pixel is set to white (0). 
Rows that do not meet these conditions (different pixel count or different color pair) 
remain unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the transformation rule to the input grid based on specific color pairs.

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

    # Define the valid color pairs for the transformation
    # Stored as a set of tuples for efficient lookup
    valid_color_pairs = {(1, 8), (8, 1), (4, 7), (7, 4)} # (Blue, Azure), (Azure, Blue), (Yellow, Orange), (Orange, Yellow)

    # Iterate through each row of the grid
    for r in range(height):
        # Find the column indices of all non-white (non-zero) pixels in the current row
        non_white_cols = np.where(input_np[r, :] != 0)[0]
        
        # Check if there are exactly two non-white pixels in this row
        if len(non_white_cols) == 2:
            # Identify the column index and color of the leftmost non-white pixel
            col_left = non_white_cols[0]
            color_left = input_np[r, col_left]
            
            # Identify the column index and color of the rightmost non-white pixel
            col_right = non_white_cols[1]
            color_right = input_np[r, col_right]

            # Check if the pair of colors (left, right) is one of the valid pairs
            if (color_left, color_right) in valid_color_pairs:
                
                # Calculate the target column index, immediately to the right of the leftmost pixel
                target_col = col_left + 1
                
                # Ensure the target column is within the grid bounds and before the rightmost pixel's original position
                # (The condition target_col < col_right implicitly covers target_col < width as col_right < width)
                if target_col < col_right:
                     # Copy the color of the rightmost pixel to the target position in the output grid
                     output_np[r, target_col] = color_right
                     
                     # Set the original position of the rightmost pixel to white (0) in the output grid
                     output_np[r, col_right] = 0
                # Handle the case where the two pixels are adjacent (target_col == col_right)
                # Although not explicitly shown in examples, if the rule holds, the move happens
                # but the target cell is immediately cleared.
                elif target_col == col_right:
                    # The color would move to output_np[r, col_right], but then gets cleared immediately.
                     output_np[r, col_right] = 0 # Clear original right pixel position

            # If the color pair is not in valid_color_pairs, do nothing (row remains as copied initially)

        # If the number of non-white pixels is not 2, do nothing (row remains as copied initially)

    # Convert the final numpy array back to a list of lists before returning
    return output_np.tolist()
