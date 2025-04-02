"""
Processes each row of the input grid independently. 
Finds the first and last occurrence of a non-white pixel in a row.
Fills the segment between these two pixels (inclusive) with the non-white color found in that row.
If a row contains no non-white pixels or only one, it remains unchanged (filled with white).
"""

import numpy as np

def transform(input_grid):
    """
    Fills the horizontal segment between the first and last non-white pixel in each row
    with that row's non-white color.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Get the dimensions of the input grid
    height, width = input_grid.shape
    
    # Initialize the output grid with the background color (white, 0)
    output_grid = np.zeros_like(input_grid) 

    # Iterate through each row of the input grid
    for r in range(height):
        row = input_grid[r, :]
        
        # Find the indices of non-white pixels in the current row
        non_white_indices = np.where(row != 0)[0]
        
        # Check if there are at least two non-white pixels in the row
        if len(non_white_indices) >= 2:
            # Get the column index of the first non-white pixel
            col1 = non_white_indices[0]
            # Get the column index of the last non-white pixel
            col2 = non_white_indices[-1]
            
            # Get the color of the first non-white pixel (assuming all non-white pixels in a row are the same color as per examples)
            fill_color = row[col1]
            
            # Fill the segment between col1 and col2 (inclusive) in the output row with the fill_color
            output_grid[r, col1 : col2 + 1] = fill_color
        elif len(non_white_indices) == 1:
             # If only one non-white pixel, copy it to the output
             col = non_white_indices[0]
             output_grid[r, col] = row[col]
        # If no non-white pixels, the output row remains white (already initialized)

    return output_grid