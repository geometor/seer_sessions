"""
Transforms an input grid by identifying all azure (8) pixels and moving them down 
by one row, changing their color to red (2) in the process. The background 
remains white (0). The output grid has the same dimensions as the input grid.
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
    height, width = input_grid.shape

    # Initialize the output grid with the background color (white, 0)
    # It should have the same dimensions as the input grid.
    output_grid = np.zeros((height, width), dtype=int)

    # Iterate through each pixel of the input grid
    for r in range(height):
        for c in range(width):
            # Check if the current pixel is azure (8)
            if input_grid[r, c] == 8:
                # Calculate the target row for the output grid (move down by 1)
                target_r = r + 1
                
                # Check if the target row is within the grid boundaries
                if target_r < height:
                    # Set the corresponding pixel in the output grid to red (2)
                    # The column remains the same.
                    output_grid[target_r, c] = 2

    # Return the completed output grid
    return output_grid
