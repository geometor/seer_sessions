"""
1.  **Identify the starting pixel:** Locate the single azure (8) pixel within the input grid.
2.  **Radiate gray pixels:** From the location of the azure pixel, extend gray (5) pixels outwards in all eight directions (up, down, left, right, and the four diagonals).
3. **Determine the shape**: The gray pixels create a combination of X and + shapes, they do not stop until the borders.
"""

import numpy as np

def find_start_pixel(grid, color=8):
    # Find the coordinates of the pixel with the specified color.
    coords = np.where(grid == color)
    if len(coords[0]) > 0:
        return coords[0][0], coords[1][0]  # Return row and column
    return None

def transform(input_grid):
    # Initialize output grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find the starting pixel (color 8)
    start_pixel = find_start_pixel(input_grid)
    if start_pixel is None:
        return output_grid # if no start pixel return
    
    start_row, start_col = start_pixel

    # Radiate outwards in all eight directions
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue  # Skip the center pixel itself

            row, col = start_row, start_col
            while 0 <= row < rows and 0 <= col < cols:
                output_grid[row, col] = 5
                row += dr
                col += dc

    output_grid[start_row, start_col] = 8 #restore the starting pixel

    return output_grid