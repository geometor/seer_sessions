"""
Compares corresponding pixels from the left and right halves of the input grid 
(separated by a central blue line at column index 3) to generate the output grid. 
The output grid has the same height as the input and a width of 3. A pixel at 
(r, c) in the output is set to green (3) if and only if the corresponding pixels 
at (r, c) in the left section (columns 0-2) and (r, c + 4) in the right section 
(columns 4-6) of the input grid are both white (0). Otherwise, the output pixel 
is white (0).
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on a pixel-wise comparison 
    between its left and right sections.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list of integers.

    Returns:
        list of lists: The transformed output grid.
    """
    # Convert input list of lists to a numpy array for easier slicing and manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Get the dimensions of the input grid
    height, width = input_np.shape
    
    # Define the width of the output grid (which is the width of the left section)
    output_width = 3 
    
    # Initialize the output grid with white (0) pixels
    # Dimensions: same height as input, width = 3
    output_grid = np.zeros((height, output_width), dtype=int)
    
    # Define the starting column index for the right section
    right_section_start_col = 4 # Column index 3 is the separator

    # Iterate through each row and the columns of the output grid (0 to output_width - 1)
    for r in range(height):
        for c in range(output_width):
            # Get the color of the pixel in the left section
            left_pixel_color = input_np[r, c]
            
            # Get the color of the corresponding pixel in the right section
            # The corresponding column in the right section is c + right_section_start_col
            right_pixel_color = input_np[r, c + right_section_start_col]
            
            # Check if both the left and right corresponding pixels are white (0)
            if left_pixel_color == 0 and right_pixel_color == 0:
                # If both are white, set the corresponding output pixel to green (3)
                output_grid[r, c] = 3
            # Else: the output pixel remains white (0) as initialized

    # Convert the numpy array back to a list of lists for the final output format
    return output_grid.tolist()
