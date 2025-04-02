"""
Processes the input grid row by row. 
For each row:
1. Finds all non-white pixels (color > 0).
2. If a row contains two or more non-white pixels:
   a. Determines their color (assumes a single non-white color per row).
   b. Finds the leftmost (minimum column index) and rightmost (maximum column index) non-white pixel.
   c. Fills the segment between the leftmost and rightmost pixel (inclusive) with that color in the output grid.
3. If a row contains fewer than two non-white pixels, it is copied directly to the output grid without modification.
The output grid has the same dimensions as the input grid.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the fill-horizontal-span transformation to the input grid.

    Args:
        input_grid (list of lists): A 2D list representing the input grid.

    Returns:
        list of lists: A 2D list representing the transformed output grid.
    """
    # Convert input list of lists to a NumPy array for easier processing
    input_array = np.array(input_grid, dtype=int)
    # Initialize the output array as a copy of the input
    output_array = np.copy(input_array)
    
    # Get the dimensions of the grid
    height, width = input_array.shape

    # Process each row independently
    for r in range(height):
        # Find the column indices of non-white pixels in the current row
        non_white_cols = np.where(input_array[r, :] > 0)[0]

        # Check if there are at least two non-white pixels
        if len(non_white_cols) >= 2:
            # Get the color of the non-white pixels (assuming they are all the same color in a row)
            # We take the color of the first non-white pixel found
            fill_color = input_array[r, non_white_cols[0]]
            
            # Find the minimum (leftmost) and maximum (rightmost) column index
            min_col = np.min(non_white_cols)
            max_col = np.max(non_white_cols)
            
            # Fill the span between min_col and max_col (inclusive) in the output row
            output_array[r, min_col:max_col+1] = fill_color
        # else: If fewer than 2 non-white pixels, the row remains unchanged (already copied)

    # Convert the output NumPy array back to a list of lists
    output_grid = output_array.tolist()
    
    return output_grid
