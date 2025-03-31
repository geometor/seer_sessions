"""
Transforms an input grid by changing red (2) or blue (1) pixels to azure (8) 
if they are horizontally adjacent (directly to the left or right) to an azure (8) pixel 
in the original input grid. All other pixels remain unchanged.
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
    # Convert input to a numpy array for easier handling
    input_np = np.array(input_grid, dtype=int)
    # Initialize the output grid as a copy of the input grid
    output_grid = np.copy(input_np)
    
    # Get grid dimensions
    height, width = input_np.shape

    # Iterate through each cell of the input grid
    for r in range(height):
        for c in range(width):
            # Get the color of the current cell in the input grid
            current_color = input_np[r, c]

            # Check if the current cell's color is red (2) or blue (1)
            if current_color == 2 or current_color == 1:
                # Initialize flags for neighbor check
                left_is_azure = False
                right_is_azure = False

                # Check left neighbor (if it exists)
                if c > 0:
                    if input_np[r, c - 1] == 8: # Check if left neighbor is azure (8)
                        left_is_azure = True
                
                # Check right neighbor (if it exists)
                if c < width - 1:
                    if input_np[r, c + 1] == 8: # Check if right neighbor is azure (8)
                        right_is_azure = True

                # If either the left or right neighbor is azure in the input grid,
                # change the corresponding cell in the output grid to azure (8)
                if left_is_azure or right_is_azure:
                    output_grid[r, c] = 8
            
            # No action needed for other colors or if the condition isn't met, 
            # as the output_grid already holds the original value.

    # Return the modified grid
    return output_grid.tolist() # Convert back to list of lists if required by ARC standards