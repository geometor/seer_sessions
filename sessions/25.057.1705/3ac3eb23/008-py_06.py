"""
1.  **Identify the initial yellow pixel:** Find the single yellow (4) pixel in the input grid.
2.  **Vertical Alternation:** Starting from the row immediately below the initial yellow pixel, and for every alternate row afterwards, change the color of the pixel in that column to yellow (4). All the way down to the bottom row of the grid.
3. **All other pixels:** All other cells remain the same color (white).
"""

import numpy as np

def find_yellow_pixel(grid):
    # Find the coordinates of the yellow pixel (value 4).
    for r in range(len(grid)):
        for c in range(len(grid[0])):
          if grid[r][c] == 4:
            return (r,c)
    return None

def transform(input_grid):
    # Create a copy of the input grid to serve as the output grid.
    output_grid = np.copy(input_grid)
    
    # Find initial yellow pixel.
    yellow_pixel_coords = find_yellow_pixel(input_grid)
    if yellow_pixel_coords is not None:
        start_row, col = yellow_pixel_coords

        # Alternate colors vertically.
        for row in range(start_row + 1, len(output_grid)):
            if (row - start_row) % 2 != 0:  #every other cell from start
                output_grid[row, col] = 4

    return output_grid