"""
1.  **Identify** the single non-white pixel (the "colored pixel") in the input grid and note its row and column indices.
2.  **Create** an output grid. It has the dimensions as the number of columns of the input, applied both as rows and columns.
3.  **Copy** the colored pixel from the input grid to its original location in the output grid.
4.  **Fill** all cells in the first row of output grid with the value 4 (yellow).
5. **Fill** cells in the columns with index equal to the "colored_pixel column index" with the value 4 (yellow).
"""

import numpy as np

def find_colored_pixel(grid):
    # Find the coordinates of the non-white pixel.
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0:
                return r, c
    return None  # Should not happen, as per problem definition.

def transform(input_grid):
    # Find the colored pixel's coordinates.
    colored_pixel_row, colored_pixel_col = find_colored_pixel(input_grid)

    # determine output grid dimensions
    output_size = input_grid.shape[1]

    # Initialize the output grid with all zeros.
    output_grid = np.zeros((output_size, output_size), dtype=int)


    # Copy the colored pixel to the output grid.
    output_grid[colored_pixel_row, colored_pixel_col] = input_grid[colored_pixel_row, colored_pixel_col]

    # Fill the first row with yellow (4).
    output_grid[0, :] = 4

    # Fill the specific column with yellow (4)
    output_grid[:,colored_pixel_col] = 4

    return output_grid