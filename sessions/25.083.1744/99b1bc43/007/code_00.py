"""
1.  **Identify Separator:** Find the horizontal row of yellow (4) pixels. This divides the input grid into "top region" and "bottom region".
2.  **Output Dimensions:** The output grid has the same dimensions (width and height) as the *bottom region* of the input grid. Initialize the output grid with all zeros.
3.  **Iterate Top Region:** Examine each pixel in the top region.
4.  **Transform Blue Pixels:** If a pixel in the top region is blue (1), change the pixel at the *same row and column* in the output grid to green (3).
5.  **Transform White Pixels:** If a pixel in the top region is white (0), copy the value of the pixel from the *same row and column* in the *bottom region* of the *input grid* to the *same row and column* in the output grid.
6.  **Other Pixels:** If the pixel in the top region is not white or blue, do not affect the output (it stays 0). The output grid should have already been initialized with all zero values.
7. **Output Complete:** After iterating over the entire top region, the output grid is complete.
"""

import numpy as np

def find_yellow_row(grid):
    """Finds the row index of the first all-yellow (4) row."""
    for i, row in enumerate(grid):
        if all(pixel == 4 for pixel in row):
            return i
    return None

def transform(input_grid):
    # Identify Separator: Find the yellow row.
    yellow_row_index = find_yellow_row(input_grid)

    # Determine Output Size: Based on the bottom region.
    top_height = yellow_row_index
    bottom_height = input_grid.shape[0] - yellow_row_index - 1
    output_height = bottom_height
    output_width = input_grid.shape[1]

    # Initialize the output grid with zeros.
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Iterate through the top region.
    for i in range(top_height):
        for j in range(output_width):
            # Transform Blue Pixels
            if input_grid[i, j] == 1:  # Blue to green
                output_grid[i, j] = 3
            # Transform White Pixels
            elif input_grid[i, j] == 0:
                output_grid[i, j] = input_grid[yellow_row_index + 1 + i, j]

    return output_grid