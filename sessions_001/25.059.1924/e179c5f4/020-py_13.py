"""
1.  **Identify the Seed:** Find the (x, y) coordinates of the single blue pixel (color 1) within the input grid. This is the "seed" of the cross.
2.  **Initialize the Output:** Create an output grid with the same dimensions as the input grid. Fill the entire output grid with azure (color 8).
3.  **Draw Vertical Line:** Starting from the seed's y-coordinate, draw a vertical line of blue (color 1) pixels upwards and downwards. The lines stop at the boundaries of the input grid.
4.  **Draw Horizontal Line:** Starting from the seed's x-coordinate, draw a horizontal line of blue (color 1) pixels to the left and to the right. The lines stop at the boundaries of the input grid.
5. **Replace Seed:** change the value of the seed pixel in the output grid to azure.
"""

import numpy as np

def find_pixel(grid, color):
    # Find the coordinates of a specific color pixel.
    for y, row in enumerate(grid):
        for x, pixel in enumerate(row):
            if pixel == color:
                return x, y
    return None

def transform(input_grid):
    # Initialize output_grid with azure (8).
    output_grid = np.full(np.shape(input_grid), 8)
    input_height, input_width = input_grid.shape

    # Find the coordinates of the blue (1) pixel.
    seed_x, seed_y = find_pixel(input_grid, 1)

    # Draw Vertical Line.
    for y in range(input_height):
        output_grid[y, seed_x] = 1

    # Draw Horizontal Line
    for x in range(input_width):
        output_grid[seed_y, x] = 1
        
    # Replace Seed
    output_grid[seed_y, seed_x] = 8

    return output_grid