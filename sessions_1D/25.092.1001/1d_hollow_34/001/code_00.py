"""
For each row in the input grid, identify the contiguous horizontal block of a single non-white color. 
Create an output grid of the same dimensions, initially filled with white (0). 
In the output grid, place the color of the identified block only at the starting and ending column indices of that block in the corresponding row. All other pixels in the output row remain white. 
If a row in the input grid contains no non-white pixels, the corresponding row in the output grid will be entirely white.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by keeping only the endpoints of horizontal non-white segments.

    Args:
        input_grid (list of lists or np.array): The input grid containing integer color values.

    Returns:
        np.array: The transformed grid.
    """
    # Convert input to numpy array for easier processing
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Initialize the output grid with the background color (white, 0)
    output_grid = np.zeros_like(input_np)

    # Iterate through each row of the input grid
    for r in range(height):
        row = input_np[r, :]
        
        # Find indices of non-white pixels in the current row
        non_white_indices = np.where(row != 0)[0]

        # Check if there are any non-white pixels in the row
        if non_white_indices.size > 0:
            # Find the start and end column indices of the block
            start_col = np.min(non_white_indices)
            end_col = np.max(non_white_indices)
            
            # Get the color of the block (using the color at the start index)
            block_color = row[start_col]
            
            # Set the corresponding pixels in the output grid row
            # Place the block color at the start column
            output_grid[r, start_col] = block_color
            # Place the block color at the end column
            output_grid[r, end_col] = block_color
            # Note: If start_col == end_col (block length 1), this correctly sets the single pixel.

    return output_grid.tolist() # Return as list of lists, common ARC format