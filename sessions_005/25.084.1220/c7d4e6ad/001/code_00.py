"""
Transformation Rule: Replace every gray pixel (color 5) in the input grid 
with the color found in the first column (column 0) of the same row. 
All other pixels remain unchanged.
"""

import numpy as np

def transform(input_grid):
    """
    Replaces gray pixels (5) with the color from the first column of the same row.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Create a copy of the input grid to initialize the output grid
    # This ensures that non-gray pixels are preserved
    output_grid = np.copy(input_grid)
    
    # Get the dimensions of the grid
    height, width = input_grid.shape
    
    # Iterate through each cell of the grid
    for r in range(height):
        for c in range(width):
            # Check if the current pixel in the input grid is gray (5)
            if input_grid[r, c] == 5:
                # Get the color from the first column (index 0) of the current row
                template_color = input_grid[r, 0]
                # Update the corresponding pixel in the output grid with the template color
                output_grid[r, c] = template_color
                
    # Return the modified grid
    return output_grid
