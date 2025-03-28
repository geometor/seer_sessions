"""
Combine information from the top and bottom halves of the input grid.
1. Divide the 12x4 input grid into two 6x4 grids: the top half (rows 0-5) and the bottom half (rows 6-11).
2. Create a new 6x4 output grid, initializing all its pixels to white (0).
3. For each row index `r` from 0 to 5 and each column index `c` from 0 to 3:
   a. If the pixel at position (`r`, `c`) in the top half grid is not white (0) OR 
      the pixel at position (`r`, `c`) in the bottom half grid is not white (0), 
      set the pixel at position (`r`, `c`) in the output grid to yellow (4).
   b. Otherwise, the pixel remains white (0).
4. Return the completed 6x4 output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by combining its top and bottom halves based on non-white pixels.

    Args:
        input_grid (list or np.ndarray): A 12x4 grid represented as a list of lists or numpy array.

    Returns:
        np.ndarray: A 6x4 grid representing the transformed output.
    """
    # Convert input to numpy array for easier slicing
    input_array = np.array(input_grid, dtype=int)
    
    # Get dimensions
    input_height = input_array.shape[0]
    input_width = input_array.shape[1]
    
    # Calculate the midpoint height
    output_height = input_height // 2
    output_width = input_width
    
    # Split the input grid into top and bottom halves
    top_half = input_array[:output_height, :]
    bottom_half = input_array[output_height:, :]
    
    # Initialize the output grid with white (0)
    output_grid = np.zeros((output_height, output_width), dtype=int)
    
    # Iterate through each cell of the output grid dimensions
    for r in range(output_height):
        for c in range(output_width):
            # Check the corresponding pixel in the top half
            pixel_top = top_half[r, c]
            # Check the corresponding pixel in the bottom half
            pixel_bottom = bottom_half[r, c]
            
            # Apply the combination logic: if either pixel is non-white (not 0)
            if pixel_top != 0 or pixel_bottom != 0:
                # Set the output pixel to yellow (4)
                output_grid[r, c] = 4
                
    return output_grid.tolist() # Return as list of lists if required by the environment