"""
Identifies white cells (0) that form the inner corner of an L-shape 
made of azure cells (8) and changes their color to blue (1). 
An inner corner is defined as a white cell having at least one 
azure neighbor vertically (up or down) AND at least one azure 
neighbor horizontally (left or right). All other cells retain 
their original color.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on the inner corner rule.

    Args:
        input_grid (list of lists or np.array): The input grid.

    Returns:
        np.array: The transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_np)
    
    # Get grid dimensions
    height, width = input_np.shape

    # Iterate through each cell (pixel) of the input grid
    for r in range(height):
        for c in range(width):
            # Check if the current cell is white (0)
            if input_np[r, c] == 0:
                # Initialize flags for neighbor checks
                has_vertical_azure = False
                has_horizontal_azure = False

                # Check vertical neighbors (up and down)
                # Check up neighbor
                if r > 0 and input_np[r - 1, c] == 8:
                    has_vertical_azure = True
                # Check down neighbor (only if up neighbor wasn't azure)
                if not has_vertical_azure and r < height - 1 and input_np[r + 1, c] == 8:
                    has_vertical_azure = True

                # Check horizontal neighbors (left and right)
                # Check left neighbor
                if c > 0 and input_np[r, c - 1] == 8:
                    has_horizontal_azure = True
                # Check right neighbor (only if left neighbor wasn't azure)
                if not has_horizontal_azure and c < width - 1 and input_np[r, c + 1] == 8:
                    has_horizontal_azure = True

                # If both vertical and horizontal azure neighbors exist
                if has_vertical_azure and has_horizontal_azure:
                    # Change the color of the corresponding cell in the output grid to blue (1)
                    output_grid[r, c] = 1

    # Return the final output grid
    return output_grid.tolist() # Convert back to list of lists if required by testing framework