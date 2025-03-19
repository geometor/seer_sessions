# a1570a43 • 008 • refine_coder

---
```python
"""
1.  **Identify Red Pixels:** Locate all pixels with the color red (value 2) in the input grid.
2.  **Determine Grid Center:** Calculate the center point of the input grid. The center is calculated as ( (height-1)/2, (width-1)/2 ).
3.  **Rotate 180 Degrees (or reflect):** Rotate the *entire set* of red pixels 180 degrees around the calculated center of the *grid*. Alternatively, a reflection across both the horizontal and vertical axes centered on the grid would achieve the same result.
4.  **Output:** Place the transformed red pixels in the output grid. All other pixels in the output grid remain unchanged from the input. Pixels that were red in the input grid but do not have a corresponding position after transformation are set to 0 (white).
"""

import numpy as np

def find_red_pixels(grid):
    # Find coordinates of all red pixels.
    return np.argwhere(grid == 2)

def calculate_center(grid):
    # Calculates the center coordinates of a grid.
    height, width = grid.shape
    center_y = (height - 1) / 2
    center_x = (width - 1) / 2
    return center_y, center_x

def rotate_180(point, center):
    # Rotate a point 180 degrees around a center.
    y, x = point
    center_y, center_x = center
    new_y = 2 * center_y - y
    new_x = 2 * center_x - x
    return (new_y, new_x)


def transform(input_grid):
    # Initialize the output grid as a copy of the input.
    output_grid = np.copy(input_grid)

    # Find all red pixels
    red_pixels = find_red_pixels(input_grid)

    # Calculate the center of the grid
    center = calculate_center(input_grid)

    # Rotate/Reflect each red pixel and update output grid
    for y, x in red_pixels:
      output_grid[y,x] = 0 # clear original position

    for point in red_pixels:
        new_point = rotate_180(point, center)

        # Ensure new point is within grid
        if 0 <= new_point[0] < output_grid.shape[0] and 0 <= new_point[1] < output_grid.shape[1]:
            output_grid[int(new_point[0]), int(new_point[1])] = 2


    return output_grid
```
