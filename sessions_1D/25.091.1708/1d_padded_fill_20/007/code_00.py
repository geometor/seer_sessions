"""
Transformation rule:
Iterate through each row of the input grid. If a row contains exactly two non-white pixels (value != 0), and both pixels have the same color value, then fill the horizontal segment between these two pixels (inclusive) with that color in the corresponding row of the output grid. Otherwise, the row remains unchanged. The output grid starts as a copy of the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the transformation rule to connect pairs of same-colored pixels within each row.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    
    # Get the dimensions of the grid
    height, width = input_grid.shape

    # Iterate through each row
    for r in range(height):
        # Select the current row from the input grid
        row = input_grid[r, :]
        
        # Find column indices of non-white pixels in the current row
        non_white_indices = np.where(row != 0)[0]
        
        # Check if there are exactly two non-white pixels in this row
        if len(non_white_indices) == 2:
            # Get the column indices of the two non-white pixels
            idx1, idx2 = non_white_indices
            
            # Get the colors of these two pixels from the input row
            color1 = row[idx1]
            color2 = row[idx2]
            
            # Check if both non-white pixels have the same color
            if color1 == color2:
                # The color to fill with is the color of the pair
                fill_color = color1
                
                # Determine the start (min) and end (max) columns for filling
                min_col = min(idx1, idx2)
                max_col = max(idx1, idx2)
                
                # Fill the segment in the corresponding row of the output grid
                # NumPy slicing is [start:end], where end is exclusive. 
                # To include max_col, we slice up to max_col + 1.
                output_grid[r, min_col : max_col + 1] = fill_color
                
        # If the conditions (exactly 2 non-white pixels, same color) are not met for this row,
        # the corresponding row in output_grid remains unchanged (as it was copied initially).
                
    # Return the modified grid
    return output_grid