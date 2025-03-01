# 3428a4f5 • 025 • refine_coder

---
```python
"""
1.  **Identify Input:** We have an input grid of varying dimensions, containing a single black (0) pixel, and all other pixels are of a single color (green (3), red (2), or yellow(4)).

2.  **Find Black Pixel:** Locate the row and column indices (coordinates) of the black pixel within the input grid.

3. **Determine Output Grid height**:
    the output grid height will be one-half of the number of rows above
    the black pixel plus one-half the number of rows below the black pixel,
    plus one for the row containing the black pixel.
    If the black pixel is in the top row, one-half of rows above is zero.
    If the black pixel is in the bottom row, one-half of rows below is zero.

4.  **Determine Output Grid width**:
    the output grid width will be one-half of the number of columns to the left of
    the black pixel plus one-half the number of columns to the right of the black pixel,
    plus one for the column containing the black pixel.
    If the black pixel is in the leftmost column, one-half of columns to the left is zero.
    If the black pixel is in the rightmost column, one-half of columns to the right is zero.

5.  **Create Output Grid:** Create an output grid filled entirely with green (3) pixels, with the dimensions determined in steps 3 & 4.

6.  **Place Black Pixel in Output Grid:**
    Place the black (0) pixel in the output grid.

7. **Determine Output Black Pixel row**:
      - count the number of rows above the black pixel in the input grid
      - the row for the black pixel in the output grid is one-half the
        number of rows counted in the previous step

8. **Determine Output Black Pixel column**:
      - count the number of columns to the left of the black pixel in the input grid
      - the column for the black pixel in the output grid is one-half the
        number of columns counted in the previous step
9. All values are integers, so use integer division.
"""

import numpy as np

def find_black_pixel(grid):
    # Find the coordinates of the black pixel (0)
    black_pixels = np.argwhere(grid == 0)
    if len(black_pixels) > 0:
      return black_pixels[0]
    else:
      return None

def determine_output_dimensions(input_grid, black_pixel_coords):
    # Calculate output grid dimensions based on black pixel position
    input_height, input_width = input_grid.shape
    if black_pixel_coords is not None:
        black_row, black_col = black_pixel_coords

        output_height = (black_row // 2) + ((input_height - 1 - black_row) // 2) + 1
        output_width = (black_col // 2) + ((input_width - 1 - black_col) // 2) + 1
    else: # Handle cases where there's no black pixel (shouldn't happen in this task)
        output_height = input_height
        output_width = input_width

    return output_height, output_width

def transform(input_grid):
    # Find black pixel coordinates in the input grid
    black_pixel_coords = find_black_pixel(input_grid)

    # Determine output grid dimensions
    output_height, output_width = determine_output_dimensions(input_grid, black_pixel_coords)

    # Create an output grid filled with green (3)
    output_grid = np.full((output_height, output_width), 3, dtype=int)
    
    if black_pixel_coords is not None:

      # Calculate the black pixel's position in the output grid
      input_black_row, input_black_col = black_pixel_coords
      output_black_row = input_black_row // 2
      output_black_col = input_black_col // 2

      # Place the black pixel in the output grid
      output_grid[output_black_row, output_black_col] = 0

    return output_grid
```
