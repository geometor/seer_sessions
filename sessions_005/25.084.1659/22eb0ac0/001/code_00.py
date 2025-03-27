"""
For each row in the input grid:
1. Check the color of the pixel in the first column (leftmost) and the color of the pixel in the last column (rightmost).
2. If both pixels are the *same* color AND that color is *not* white (0), then fill the entire corresponding row in the output grid with that color.
3. Otherwise (if the colors are different, or one/both are white), the row in the output grid remains identical to the input row.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on matching colors at the ends of each row.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_grid_np = np.array(input_grid)
    
    # Get grid dimensions
    height, width = input_grid_np.shape
    
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid_np)

    # Iterate through each row of the input grid
    for r in range(height):
        # Get the color of the first (leftmost) pixel in the current row
        first_pixel_color = input_grid_np[r, 0]
        
        # Get the color of the last (rightmost) pixel in the current row
        last_pixel_color = input_grid_np[r, width - 1]
        
        # Check if the first and last pixels have the same color,
        # and that color is not white (0)
        if first_pixel_color == last_pixel_color and first_pixel_color != 0:
            # If the condition is met, fill the entire row in the output grid
            # with the matching color
            output_grid[r, :] = first_pixel_color
        # Else (colors are different or one/both are white), 
        # the output row remains as copied from the input, so no action needed here.

    return output_grid.tolist() # Convert back to list of lists if needed, based on expected format
