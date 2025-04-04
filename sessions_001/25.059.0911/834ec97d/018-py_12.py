"""
1.  **Find the Maroon Pixel:** Locate the single maroon (color value 9) pixel within the input grid.  Its position (row and column) should be preserved in the output grid.
2.  **Determine Grid Width:** Get the width of the input grid.
3. **Determine Rows Above:** Calculate number of rows above maroon pixel.
4.  **Create Alternating Rows:** Generate rows with alternating yellow (4) and white (0) pixels. The length of each row should match the input grid's width.  The sequence *always* starts with yellow. The number of the alternating rows is equal to the number of rows above the maroon pixel.
5.  **Fill Above Maroon Pixel:** Fill the space in the output grid *above* the maroon pixel with the alternating rows. Start with yellow row at the top, then white, repeating until the row below the top row.
6. **Preserve Maroon Pixel**: Ensure that only space above the maroon pixel is replaced.
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
    # Initialize output_grid as a copy of the input.
    output_grid = np.copy(input_grid)
    
    # Find the location of the maroon pixel (value 9).
    maroon_location = find_pixel_location(input_grid, 9)
    
    # Get the width of the input grid.
    grid_width = input_grid.shape[1]

    if maroon_location:
        # Determine the number of rows above the maroon pixel.
        rows_above = maroon_location[1]

        # Create alternating rows of yellow and white.
        for i in range(rows_above):
            row_pattern = [4 if (i+j) % 2 == 0 else 0 for j in range(grid_width)]
            output_grid[i] = row_pattern
    
    return output_grid