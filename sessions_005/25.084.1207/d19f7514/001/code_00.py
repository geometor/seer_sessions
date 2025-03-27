"""
Divide the input grid vertically into two equal halves: a top_grid (rows 0 to 5) 
and a bottom_grid (rows 6 to 11). Create a new output grid with the same 
dimensions as the top_grid (6 rows, 4 columns), initially filled with white (0).
Iterate through each cell (pixel) position (row, column). If the pixel at the 
current position in the top_grid is green (3) OR the pixel at the corresponding 
position in the bottom_grid is gray (5), set the pixel at the current position 
in the output grid to yellow (4). Otherwise, the output pixel remains white (0).
Return the completed output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of lists or numpy array): The input grid.

    Returns:
        numpy array: The transformed output grid.
    """
    # Convert input to numpy array for easier slicing
    input_array = np.array(input_grid, dtype=int)
    
    # Get the dimensions
    input_height, input_width = input_array.shape
    
    # Calculate the midpoint height
    mid_height = input_height // 2
    output_height = mid_height
    output_width = input_width
    
    # Split the input grid into top and bottom halves
    top_grid = input_array[:mid_height, :]
    bottom_grid = input_array[mid_height:, :]
    
    # Initialize the output grid with white (0)
    output_grid = np.zeros((output_height, output_width), dtype=int)
    
    # Iterate through each pixel position in the output grid dimensions
    for r in range(output_height):
        for c in range(output_width):
            # Get the corresponding pixel values from the top and bottom input grids
            top_pixel = top_grid[r, c]
            bottom_pixel = bottom_grid[r, c]
            
            # Apply the transformation rule:
            # If top is green (3) OR bottom is gray (5), output is yellow (4)
            if top_pixel == 3 or bottom_pixel == 5:
                output_grid[r, c] = 4
            # Otherwise, the output remains white (0) as initialized
            
    return output_grid
