"""
The transformation rule involves filtering elements based on their position relative to a horizontal line of '5's. 
Only azure ('8') and blue ('1') pixels above the line of '5's are retained in the output grid.
'1' is added to output directly above or below '8'
The remaining cells are filled with '0'.
"""

import numpy as np

def find_object_by_color(grid, color):
    """Finds coordinates of all pixels of a specific color."""
    return np.argwhere(grid == color)

def transform(input_grid):
    # Initialize output grid with zeros (white)
    output_grid = np.zeros_like(input_grid)

    # Find the line of 5s
    line_of_5s = find_object_by_color(input_grid, 5)
    if line_of_5s.size > 0:
        # Determine the row index of the line of 5s (assuming it's a single horizontal line)
        row_of_5s = line_of_5s[0][0]

        # Find azure (8) and blue (1) pixels
        azure_pixels = find_object_by_color(input_grid, 8)
        blue_pixels = find_object_by_color(input_grid, 1)

        # Filter pixels above the line of 5s
        filtered_azure_pixels = [p for p in azure_pixels if p[0] < row_of_5s]
        filtered_blue_pixels = [p for p in blue_pixels if p[0] < row_of_5s]
        
        # Copy filtered pixels to the output grid
        for r, c in filtered_azure_pixels:
            output_grid[r, c] = 8
        for r, c in filtered_blue_pixels:
            output_grid[r, c] = 1

        # add 1's above and below 8's
        for r, c in filtered_azure_pixels:
            if r > 0:
                output_grid[r-1, c] = 1
            if r < output_grid.shape[0]-1:
                output_grid[r+1,c] = 1

    return output_grid