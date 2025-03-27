"""
Transforms the input grid by finding non-white pixels in the *input* grid and extending a horizontal alternating pattern (gray, original_color) to their right in the *output* grid.

1. Initialize the output grid as an identical copy of the input grid.
2. Iterate through each row (r) and column (c) of the *input* grid.
3. If the pixel at (r, c) in the *input* grid is not white (color is not 0):
    a. Let the color of this pixel be original_color. This is a "trigger pixel".
    b. Iterate through the columns c_new in the *output* grid, starting from c + 1 to the last column index.
    c. Calculate the horizontal distance: distance = c_new - c.
    d. Determine the color to place at (r, c_new) in the *output* grid:
        i. If the distance is odd, set the color to gray (5).
        ii. If the distance is even, set the color to the original_color of the trigger pixel.
    e. Update the pixel at (r, c_new) in the *output* grid with the determined color.
4. After checking all pixels in the input grid, return the final output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Applies a horizontal alternating pattern transformation based on non-white pixels.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input grid
    # Modifications will be made to this grid
    output_grid = input_grid_np.copy()
    
    # Get the dimensions of the grid
    height, width = input_grid_np.shape

    # Iterate through each pixel of the *input* grid to find triggers
    for r in range(height):
        for c in range(width):
            # Check if the pixel in the *input* grid is not white (color 0)
            if input_grid_np[r, c] != 0:
                original_color = input_grid_np[r, c] # Store the trigger color
                
                # Iterate through the columns to the right of the trigger pixel in the *output* grid
                for c_new in range(c + 1, width):
                    # Calculate the horizontal distance from the trigger pixel
                    distance = c_new - c
                    
                    # Determine the color based on the distance (alternating pattern)
                    if distance % 2 == 1:
                        # Odd distance: set to gray (5) in the output grid
                        output_grid[r, c_new] = 5
                    else:
                        # Even distance: set to the original color in the output grid
                        output_grid[r, c_new] = original_color

    # Convert the numpy array back to a list of lists for the expected output format
    return output_grid.tolist()