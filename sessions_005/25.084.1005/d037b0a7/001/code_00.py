"""
Processes a grid column by column. For each column, it scans from top to bottom. 
It keeps track of the last non-white color encountered ('current_paint_color'). 
If a white pixel (0) is found, it is changed to the 'current_paint_color', 
provided that 'current_paint_color' is not white. 
Non-white pixels update the 'current_paint_color' and retain their original color.
"""

import numpy as np

def transform(input_grid):
    """
    Applies a vertical color dripping effect to the input grid.

    Args:
        input_grid (list of lists or np.array): The input grid.

    Returns:
        np.array: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    
    # Create a copy of the input grid to modify, ensuring the original is untouched
    output_grid = input_array.copy()
    
    # Get the dimensions of the grid
    height, width = output_grid.shape
    
    # Define the white color value
    white = 0
    
    # Iterate through each column index
    for c in range(width):
        # Initialize the 'current_paint_color' for this column to white
        current_paint_color = white
        
        # Iterate through each row index within the current column, from top to bottom
        for r in range(height):
            # Get the color of the pixel in the original input grid
            input_pixel_color = input_array[r, c]
            
            # Check if the input pixel is non-white
            if input_pixel_color != white:
                # Update the current paint color to this pixel's color
                current_paint_color = input_pixel_color
            # Else (if the input pixel is white)
            else:
                # Check if the current paint color is non-white
                if current_paint_color != white:
                    # Change the color of the corresponding pixel in the output grid
                    output_grid[r, c] = current_paint_color
                    
    # Return the modified output grid
    return output_grid.tolist() # Convert back to list of lists if needed by the environment
