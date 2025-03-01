"""
1.  Identify: Find all yellow (4) and red (2) pixels in the input grid.
2.  Extend Downwards Conditionally: For each yellow or red pixel, copy its color to the cells directly below it in the same column.
3.  Stopping Condition: Stop extending the color downwards when a black (1) pixel is encountered or the bottom of the grid is reached.
4. Preserve other colors: If the color is any color other than yellow or red, leave it unchanged.
"""

import numpy as np

def transform(input_grid):
    """Transforms the input grid by extending yellow and red colors downwards until a black pixel or the bottom is reached."""
    output_grid = np.copy(input_grid)  # Initialize output_grid as a copy of the input_grid
    rows, cols = output_grid.shape

    # Iterate through each column
    for j in range(cols):
        # Iterate through each row in the column
        for i in range(rows):
            # Extend yellow color downwards
            if input_grid[i, j] == 4:  # Check for yellow pixel
                for k in range(i + 1, rows):  # Iterate downwards from current position
                    if output_grid[k, j] == 1: # Check for black pixel
                        break  # Stop extending if black pixel is encountered
                    output_grid[k, j] = 4  # Set the pixel to yellow

            # Extend red color downwards
            elif input_grid[i, j] == 2:  # Check for red pixel
                for k in range(i + 1, rows): # Iterate downwards from current position
                    if output_grid[k,j] == 1:  #check for black pixel
                        break  # Stop extending if black pixel is encountered.
                    output_grid[k, j] = 2  # Set the pixel to red

    return output_grid