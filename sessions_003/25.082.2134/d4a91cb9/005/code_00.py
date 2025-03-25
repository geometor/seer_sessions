"""
1.  **Find Non-Black Pixels**: Locate all pixels in the input grid that are not black (value 0).
2.  **Identify the Extending and Stationary Pixels**: If there are at least two non-black pixels, identify which one extends, and which one is stationary.
  *   **Extending pixel**: if non-black pixel colors are different, the extending pixel will change its color to yellow.
  *   **Stationary pixel**: This pixel will not change color.
3.  **Initial Output Grid**: Create an output grid initially filled with black pixels.
4. **Extend and Change color** Change the extending pixel to yellow (value = 4).
    *   **Horizontal/Vertical Extension**: From the new yellow pixel, extend the position either *horizontally* to the column of the *stationary* pixel, OR *vertically* to the row of the *stationary* pixel.
5.  **Fill Rectangle**: Fill the space between the extended yellow line, up to and including the stationary pixel, with yellow color.
6. **Keep Stationary Pixel**: keep the color of the stationary pixel.
7.  **Black Background**: Ensure all remaining pixels in the output grid are black (value 0).
"""

import numpy as np

def find_non_black_pixels(grid):
    """Finds the coordinates of non-black pixels."""
    return np.argwhere(grid != 0)

def get_extending_pixel(grid, non_black_pixels):
    """Determines which pixel is the extending pixel (the one to change to yellow)."""
    if len(non_black_pixels) != 2:
        return None, None

    pixel_a = non_black_pixels[0]
    pixel_b = non_black_pixels[1]

    if grid[pixel_a[0], pixel_a[1]] != grid[pixel_b[0], pixel_b[1]]:
        return pixel_a, pixel_b  # pixel_a is extending pixel, pixel_b is stationary pixel

    return None, None

def extend_and_fill(extending_pixel, stationary_pixel, output_grid):
    """Extends a line from the extending pixel and fills the rectangle."""

    # Extend vertically
    if extending_pixel[1] == stationary_pixel[1]:
        min_row = min(extending_pixel[0], stationary_pixel[0])
        max_row = max(extending_pixel[0], stationary_pixel[0])
        for row in range(min_row, max_row + 1):
            output_grid[row, extending_pixel[1]] = 4
        
    # Extend horizontally
    elif extending_pixel[0] == stationary_pixel[0]:
        min_col = min(extending_pixel[1], stationary_pixel[1])
        max_col = max(extending_pixel[1], stationary_pixel[1])
        for col in range(min_col, max_col + 1):
            output_grid[extending_pixel[0], col] = 4
    else:
      # Extend to same row
      min_row = min(extending_pixel[0], stationary_pixel[0])
      max_row = max(extending_pixel[0], stationary_pixel[0])

      if extending_pixel[0] < stationary_pixel[0]:
        for row in range(extending_pixel[0]+1, stationary_pixel[0] + 1):
          output_grid[row, extending_pixel[1]] = 4
      else:
          for row in range(stationary_pixel[0], extending_pixel[0]):
            output_grid[row, extending_pixel[1]] = 4

    # Fill rectangle
    min_row = min(extending_pixel[0], stationary_pixel[0])
    max_row = max(extending_pixel[0], stationary_pixel[0])
    min_col = min(extending_pixel[1], stationary_pixel[1])
    max_col = max(extending_pixel[1], stationary_pixel[1])

    for row in range(min_row, max_row + 1):
        for col in range(min_col, max_col + 1):
            output_grid[row, col] = 4

def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # Find non-black pixels
    non_black_pixels = find_non_black_pixels(input_grid)

    if len(non_black_pixels) < 2:
        return output_grid

    # Determine extending and stationary pixels
    extending_pixel, stationary_pixel = get_extending_pixel(input_grid, non_black_pixels)
    
    if extending_pixel is None:
      return output_grid

    # Change extending_pixel color and keep the stationary pixel
    output_grid[extending_pixel[0], extending_pixel[1]] = 4
    output_grid[stationary_pixel[0], stationary_pixel[1]] = input_grid[stationary_pixel[0], stationary_pixel[1]]

    # Extend and fill
    extend_and_fill(extending_pixel, stationary_pixel, output_grid)
    
    return output_grid