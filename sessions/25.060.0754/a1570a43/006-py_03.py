"""
1.  **Identify Red Pixels:** Locate all pixels with the color red (value 2) within the input grid.
2.  **Rotate:** For *each* red pixel, individually rotate it 90 degrees clockwise around a fixed center point.
3. **Fixed Center.** The center of rotation is at coordinates (x, y) where:
      - `x` = the x coordinate of the original red pixel
      - `y` = `input_grid.shape[1] // 2 - (red_pixel.x - input_grid.shape[0] // 2)`
      - Note, the `//` operator represents integer division.
4. **Output.** Place the rotated red pixels in the output, any existing red pixels in the input grid should be empty (value 0) in the output.
"""

import numpy as np

def find_red_pixels(grid):
    # Find coordinates of all red pixels.
    return np.argwhere(grid == 2)

def rotate_point_around_dynamic_center(point, grid_shape):
    # Rotate a point 90 degrees clockwise around a dynamic center.
    y, x = point
    center_y = y
    center_x = grid_shape[1] // 2 - (y - grid_shape[0] // 2)
    new_y = center_y + (x - center_x)
    new_x = center_x - (y - center_y)
    return (new_y, new_x)

def transform(input_grid):
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    
    # Find all red pixels
    red_pixels = find_red_pixels(input_grid)
    
    # Clear existing red pixels from output grid
    for y, x in red_pixels:
      output_grid[y,x] = 0

    # Rotate each red pixel individually and update the output grid.
    for point in red_pixels:
        new_point = rotate_point_around_dynamic_center(point, input_grid.shape)
        # Ensure the new point is within the grid bounds.
        if 0 <= new_point[0] < output_grid.shape[0] and 0 <= new_point[1] < output_grid.shape[1]:
            output_grid[new_point] = 2

    return output_grid