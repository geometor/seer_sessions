"""
1.  **Locate the Green Pixel:** Find the single pixel in the input grid that is colored green (value 3). Record its row and column coordinates.
2.  **Create Output Grid:** Generate an output grid that has identical dimensions (height and width) as the input grid. Initialize all pixels in the output grid to white (value 0).
3.  **Draw Horizontal Line:** In the output grid, draw a horizontal line using the color green (value 3). This line should span the entire width of the grid and be positioned at the row coordinate obtained in step 1.
4.  **Draw Vertical Line:** In the output grid, draw a vertical line using the color green (value 3). This line should span the entire height of the grid and be positioned at the column coordinate obtained in step 1.
5. **Output:** return the output_grid.
"""

import numpy as np

def find_green_pixel(grid):
    """Finds the coordinates of the single green pixel in a grid."""
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 3:
                return (r, c)  # Returns (row, col)
    return None  # No green pixel found

def transform(input_grid):
    # Create Output Grid: Identical dimensions, initialized to white (0)
    output_grid = np.zeros_like(input_grid)

    # Locate the Green Pixel
    green_pixel_location = find_green_pixel(input_grid)

    if green_pixel_location:  # Proceed only if a green pixel was found
        row, col = green_pixel_location

        # Draw Horizontal Line
        output_grid[row, :] = 3

        # Draw Vertical Line
        output_grid[:, col] = 3

    return output_grid