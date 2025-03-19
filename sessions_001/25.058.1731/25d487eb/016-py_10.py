"""
1.  **Locate Green Pixel:** Find the single green pixel in the input grid. Note its column.
2.  **Initialize Output:** Create an output grid, initially all white.
3.  **Draw Vertical Line Iteratively:** Starting from the top row (row 0) of the *output* grid, in the column identified in step 1, draw a green pixel.
4.  **Check for Obstacles:** After drawing *each* green pixel, check the cell immediately *below* it in the *output* grid.
5.  **Stopping Condition:**
    *   If the cell below is non-white, stop drawing the line (the current pixel is the last one).
    *   If the cell below is white, continue to the next row and repeat steps 3 and 4.
    *   If you reach the bottom row of the output grid, stop drawing.
"""

import numpy as np

def find_green_pixel(grid):
    """Finds the coordinates of the single green pixel in the grid."""
    rows, cols = np.where(grid == 3)
    if len(rows) > 0:
        return rows[0], cols[0]  # Assuming only one green pixel
    return None

def transform(input_grid):
    # Initialize output_grid as all white
    output_grid = np.zeros_like(input_grid)

    # Find the green pixel's column in the input grid
    green_pixel_coords = find_green_pixel(input_grid)
    if green_pixel_coords is None:
        return output_grid # Return blank if no green pixel
    
    _, green_col = green_pixel_coords

    # Draw the vertical line iteratively, checking for obstacles
    for row in range(output_grid.shape[0]):
        # Draw the green pixel
        output_grid[row, green_col] = 3

        # Check the cell below
        if row + 1 < output_grid.shape[0]:  # Ensure we're not at the bottom
            if output_grid[row + 1, green_col] != 0:
                break  # Stop if the cell below is not white

    return output_grid