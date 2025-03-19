"""
The transformation rule depends on the presence and location of a maroon pixel (color value 9) within the input grid.

1. **Check for Maroon Pixel:** If a maroon pixel is *not* present in the input grid, the output grid is identical to the input grid (no transformation occurs).
2. **Maroon Pixel Present:** If a maroon pixel *is* present:
   - The output grid is initialized as a copy of the input grid.
   - The rows above the maroon pixel are replaced with alternating rows of yellow (4) and white (0) pixels, starting with yellow.
   - The maroon pixel's location is preserved.
   - The rest of the grid remains unchanged.
"""

import numpy as np

def find_pixel_location(grid, color_value):
    # Find the location of a pixel with a specific color value.
    for r_idx, row in enumerate(grid):
        for c_idx, pixel in enumerate(row):
            if pixel == color_value:
                return (c_idx, r_idx)
    return None

def transform(input_grid):
    # Check for the presence of a maroon pixel.
    maroon_location = find_pixel_location(input_grid, 9)

    if maroon_location is None:
        # If no maroon pixel, return the input grid unchanged.
        return input_grid
    else:
        # Initialize output_grid as a copy of the input.
        output_grid = np.copy(input_grid)

        # Get the width of the input grid.
        grid_width = input_grid.shape[1]
        
        # Determine the number of rows above the maroon pixel.
        rows_above = maroon_location[1]

        # Create alternating rows of yellow and white and fill above.
        for i in range(rows_above):
            row_pattern = [4 if (i+j) % 2 == 0 else 0 for j in range(grid_width)]
            output_grid[i] = row_pattern
        
        return output_grid