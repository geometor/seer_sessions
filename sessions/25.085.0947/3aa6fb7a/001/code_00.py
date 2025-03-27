"""
This module transforms an input grid based on a local pattern.
It identifies 2x2 subgrids within the input grid that contain exactly three 
'azure' (8) pixels and one 'white' (0) pixel. For each such identified 
subgrid, the 'white' pixel is changed to 'blue' (1) in the output grid. 
All other pixels remain unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of lists or np.ndarray): The input grid.

    Returns:
        np.ndarray: The transformed output grid.
    """
    # Convert input to a numpy array for easier slicing and manipulation
    input_array = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_array)
    
    # Get the dimensions of the grid
    height, width = input_array.shape

    # Define the colors we are looking for
    azure_color = 8
    white_color = 0
    blue_color = 1

    # Iterate through all possible top-left corners of 2x2 subgrids
    # The range stops at height-1 and width-1 because a 2x2 grid needs 
    # indices row, row+1, col, col+1. So the max starting row is height-2 
    # and max starting col is width-2.
    for r in range(height - 1):
        for c in range(width - 1):
            # Extract the 2x2 subgrid
            subgrid = input_array[r:r+2, c:c+2]
            
            # Count the number of azure and white pixels in the subgrid
            azure_count = np.count_nonzero(subgrid == azure_color)
            white_count = np.count_nonzero(subgrid == white_color)
            
            # Check if the condition (3 azure, 1 white) is met
            if azure_count == 3 and white_count == 1:
                # Find the location of the white pixel within the 2x2 subgrid
                # np.where returns indices relative to the subgrid (0 or 1)
                white_r_rel, white_c_rel = np.where(subgrid == white_color)
                
                # Check if exactly one white pixel was found (as expected)
                if len(white_r_rel) == 1:
                    # Calculate the absolute coordinates in the full grid
                    white_r_abs = r + white_r_rel[0]
                    white_c_abs = c + white_c_rel[0]
                    
                    # Update the corresponding cell in the output grid to blue
                    output_grid[white_r_abs, white_c_abs] = blue_color

    # Return the modified output grid
    return output_grid.tolist() # Return as list of lists if required by the environment