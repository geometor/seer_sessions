"""
Transform an input grid into a larger output grid based on the following rule:

1. Initialize an output grid that is 3 times the height and 3 times the width of the input grid, filled with the background color white (0).
2. Conceptually divide the output grid into a grid of 3x3 'slots', where each slot is the same size as the input grid.
3. Iterate through each pixel (r, c) in the input grid.
4. If the color value of the input pixel at (r, c) is greater than 1, copy the *entire* original input grid into the corresponding slot in the output grid. The top-left corner of the slot corresponding to input pixel (r, c) is located at output grid coordinates (r * 3, c * 3).
5. If the color value of the input pixel at (r, c) is 0 or 1, the corresponding slot in the output grid remains filled with the background color.
6. Return the final output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Get the dimensions of the input grid
    input_height, input_width = input_grid.shape
    
    # Calculate the dimensions of the output grid (3x scaled)
    output_height = input_height * 3
    output_width = input_width * 3
    
    # Initialize the output grid with the background color (white, 0)
    output_grid = np.zeros((output_height, output_width), dtype=int)
    
    # Iterate through each pixel of the input grid
    for r in range(input_height):
        for c in range(input_width):
            # Get the color value of the current input pixel
            pixel_value = input_grid[r, c]
            
            # Check if the pixel value is greater than 1
            if pixel_value > 1:
                # Calculate the top-left coordinates for the target slot in the output grid
                start_row = r * 3
                start_col = c * 3
                
                # Calculate the bottom-right coordinates for the target slot
                end_row = start_row + input_height
                end_col = start_col + input_width
                
                # Copy the entire input grid into the calculated slot in the output grid
                output_grid[start_row:end_row, start_col:end_col] = input_grid
                
    # Return the completed output grid
    return output_grid
