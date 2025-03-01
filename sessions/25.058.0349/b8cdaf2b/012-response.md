# b8cdaf2b • 012 • refine_coder

---
```python
"""
For each green pixel in the input grid, check if the color of the pixel directly above it is the same as the color of the pixel directly below it. If they are the same color, create a vertical line of green pixels extending upwards from the original green pixel to the top edge of the grid. Pixels not meeting this condition remain unchanged.
"""

import numpy as np

def find_pixels_by_color(grid, color):
    # Find the coordinates of all pixels of the specified color.
    coords = np.argwhere(grid == color)
    return coords

def check_above_below_same_color(grid, row, col):
    # Check if the pixel is at the top or bottom edge
    if row == 0 or row == grid.shape[0] - 1:
        return False

    # Check if the colors above and below are the same
    return grid[row - 1, col] == grid[row + 1, col]

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid
    output_grid = np.copy(input_grid)

    # Find all green pixels (color 3)
    green_pixel_coords = find_pixels_by_color(input_grid, 3)

    if len(green_pixel_coords) > 0:
        for green_pixel_coord in green_pixel_coords:
            row, col = green_pixel_coord

            # Check if the colors above and below the green pixel are the same
            if check_above_below_same_color(input_grid, row, col):
                # Extend green color upwards
                for r in range(row - 1, -1, -1):
                    output_grid[r, col] = 3

    return output_grid
```
