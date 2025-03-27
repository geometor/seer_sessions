import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by finding non-white pixels and extending a horizontal pattern to their right.

    1. Initialize the output grid as a copy of the input grid.
    2. Iterate through each row (r) and column (c) of the input grid.
    3. If the pixel at (r, c) is not white (color is not 0):
        a. Let the color of this pixel be original_color.
        b. Iterate through the columns c_new from c + 1 to the last column index of the grid.
        c. Determine the color to place at (r, c_new):
            i. If the horizontal distance (c_new - c) is odd, set the color to gray (5).
            ii. If the horizontal distance (c_new - c) is even, set the color to original_color.
        d. Update the pixel at (r, c_new) in the output grid with the determined color.
    4. Return the final output grid.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input grid
    output_grid = input_grid_np.copy()
    
    # Get the dimensions of the grid
    height, width = output_grid.shape

    # Iterate through each pixel of the input grid
    for r in range(height):
        for c in range(width):
            # Check if the pixel is not white (color 0)
            if output_grid[r, c] != 0:
                original_color = output_grid[r, c]
                
                # Iterate through the columns to the right of the current pixel
                for c_new in range(c + 1, width):
                    # Calculate the horizontal distance from the original colored pixel
                    distance = c_new - c
                    
                    # Determine the color based on the distance (alternating pattern)
                    if distance % 2 == 1:
                        # Odd distance: set to gray (5)
                        output_grid[r, c_new] = 5
                    else:
                        # Even distance: set to the original color
                        output_grid[r, c_new] = original_color

    # Convert the numpy array back to a list of lists for the expected output format
    return output_grid.tolist()