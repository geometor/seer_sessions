"""
1.  **Identify the Single Green Pixel:** Find the *single* pixel in the input grid that has the color value 3 (green). Note its row and column indices.
2.  **Draw Horizontal Line:** Draw a horizontal line across the entire grid, using color 3 (green), at the row index found in step 1.
3.  **Draw Vertical Line:** Draw a vertical line down the entire grid, using color 3 (green), at the column index found in step 1.
4.  **Background:** The rest of the grid should consist of pixels with color white(0).
"""

import numpy as np

def find_single_green_pixel(grid):
    # find the single green pixel.
    rows, cols = grid.shape
    green_pixels = []
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == 3:
                green_pixels.append((r, c))
    if len(green_pixels) == 1:
        return green_pixels[0]  # Return the (row, col) tuple
    else:
        return None  # Handle cases where there isn't exactly one green pixel

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # find the green pixel location
    green_pixel_location = find_single_green_pixel(input_grid)

    # Draw the cross if a green pixel was found
    if green_pixel_location:
      row, col = green_pixel_location

      # horizontal line
      for c in range(output_grid.shape[1]):
          output_grid[row, c] = 3
      # vertical line
      for r in range(output_grid.shape[0]):
        output_grid[r, col] = 3
    
    return output_grid