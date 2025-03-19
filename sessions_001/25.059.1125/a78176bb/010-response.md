# a78176bb • 010 • example_2 • investigate_coder

---
```python
"""
The transformation identifies two shapes in the input grid: one of gray (5) pixels and another of maroon (9) pixels. The gray shape is removed (replaced with white (0)), and the maroon shape is rotated 45 degrees clockwise around its top-right corner. The background (0) remains unchanged.
"""

import numpy as np

def find_object(grid, value):
    # Find coordinates of all pixels with the given value
    coords = np.argwhere(grid == value)
    return coords

def rotate_shape_45_degrees(coords, pivot):
    # Rotate coordinates 45 degrees clockwise around a pivot point.
    # Basic formula for 45 degree rotation
    # x' = (x - a) * cos(45) - (y - b) * sin(45) + a
    # y' = (x - a) * sin(45) + (y - b) * cos(45) + b
    # Where (a,b) are the pivot x and y
    # sin(45) = cos(45) for 45 degrees = 0.7071 (approx)

    rotated_coords = []
    a, b = pivot
    for x, y in coords:
        new_x = int(round((x - a) * 0.7071 - (y - b) * 0.7071 + a))
        new_y = int(round((x - a) * 0.7071 + (y - b) * 0.7071 + b))
        rotated_coords.append((new_x, new_y))
    return rotated_coords

def transform(input_grid):
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # Find maroon (9) object
    maroon_coords = find_object(input_grid, 9)
    if len(maroon_coords) == 0:
        return output_grid

    # Remove the gray object (5)
    gray_coords = find_object(input_grid, 5)
    for x,y in gray_coords:
        output_grid[x,y] = 0

    # find pivot - the top-right maroon pixel
    min_y = np.min(maroon_coords[:, 1])
    top_maroon_coords = maroon_coords[maroon_coords[:,1] == min_y]
    min_x = np.min(top_maroon_coords[:, 0])
    pivot_coord = (min_x, min_y)


    # Rotate maroon object
    rotated_maroon_coords = rotate_shape_45_degrees(maroon_coords, pivot_coord)


    # Place rotated maroon pixels in the output grid, handling out-of-bounds
    for x, y in rotated_maroon_coords:
        if 0 <= x < output_grid.shape[0] and 0 <= y < output_grid.shape[1]:
            output_grid[x, y] = 9
        # else the rotated coordinate goes off the board

    return output_grid
```
