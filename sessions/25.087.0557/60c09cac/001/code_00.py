"""
Scales the input grid by a factor of 2 in both height and width.
Each pixel in the input grid becomes a 2x2 block of the same color in the output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms an input grid by scaling each pixel into a 2x2 block.

    Args:
        input_grid (list of lists or numpy array): The input grid.

    Returns:
        numpy array: The transformed output grid.
    """
    # Convert input_grid to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Determine the dimensions of the input grid
    input_height, input_width = input_np.shape
    
    # Calculate the dimensions of the output grid (scaled by 2)
    output_height = input_height * 2
    output_width = input_width * 2
    
    # Initialize the output grid with zeros (white color)
    output_grid = np.zeros((output_height, output_width), dtype=int)
    
    # Iterate through each pixel in the input grid
    for r in range(input_height):
        for c in range(input_width):
            # Get the color of the current input pixel
            color = input_np[r, c]
            
            # Calculate the top-left coordinates for the 2x2 block in the output grid
            out_r = r * 2
            out_c = c * 2
            
            # Fill the corresponding 2x2 block in the output grid with the color
            output_grid[out_r:out_r + 2, out_c:out_c + 2] = color
            
    return output_grid
