# 54d82841 • 010 • example_2 • investigate_coder

---
```python
"""
Identifies green (3) pixels in the input grid, finds a specific white (0) pixel based on their configuration, 
and changes that pixel's color to yellow (4). All other pixels remain unchanged. The specific white pixel is found by
considering where lines extending from the green pixels would intersect, and a pixel below and to the left of that
point is changed.
"""

import numpy as np

def find_green_pixels(grid):
    # Find coordinates of all green pixels.
    green_coords = np.argwhere(grid == 3)
    return green_coords

def find_target_pixel(grid, green_coords):
    # Find the target white pixel to change to yellow.
    if len(green_coords) == 0:
        return None

    # Find the bottom-most row containing green pixels.
    max_row = np.max(green_coords[:, 0])
    
    # Find the rightmost green pixel for horizontal line.
    rightmost_green_col = np.max(green_coords[:, 1])

    # Find bottom-most green pixels
    bottom_green_pixels = green_coords[green_coords[:,0] == max_row]
    # find left-most one of these
    leftmost_green_col = np.min(bottom_green_pixels[:,1])
    
    # find intersection point
    intersect_row = max_row
    intersect_col = rightmost_green_col

    # find location of target
    target_row = max_row + 2
    target_col = leftmost_green_col

    if (0 <= target_row < grid.shape[0] and 0 <= target_col < grid.shape[1] and grid[target_row, target_col] == 0) :
         return (target_row, target_col)
    else:
        return None

def transform(input_grid):
    # Initialize output_grid as a copy of input_grid.
    output_grid = np.copy(input_grid)

    # Find green pixels.
    green_pixels = find_green_pixels(output_grid)

    # Find the target white pixel.
    target_pixel = find_target_pixel(output_grid, green_pixels)

    # Change the target pixel to yellow if found.
    if target_pixel:
        output_grid[target_pixel[0], target_pixel[1]] = 4

    return output_grid
```
