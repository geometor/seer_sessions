# 9dfd6313 • 010 • example_2 • investigate_coder

---
```python
"""
The non-white pixels are changing their positions based on a 90 degree clockwise rotation centered around the gray pixels. The values are copied into their new locations.
"""

import numpy as np

def get_non_zero_pixels(grid):
    """
    Finds the coordinates of non-zero pixels in the grid.
    """
    coords = []
    for row_idx, row in enumerate(grid):
        for col_idx, value in enumerate(row):
            if value != 0:
                coords.append(((row_idx, col_idx), value))
    return coords

def rotate_point(point, center):
    """Rotates a point 90 degrees clockwise around a center point."""
    row, col = point
    center_row, center_col = center
    new_row = center_row + (col - center_col)
    new_col = center_col - (row - center_row)
    return (new_row, new_col)


def transform(input_grid):
    # initialize output_grid
    output_grid = np.zeros_like(input_grid)

    # Get non-zero pixels and their values.
    non_zero_pixels = get_non_zero_pixels(input_grid)

    # Find the centroid of non-zero pixels.
    rows = [coord[0][0] for coord in non_zero_pixels]
    cols = [coord[0][1] for coord in non_zero_pixels]
    center_row = sum(rows) / len(rows)
    center_col = sum(cols) / len(cols)
    center = (center_row, center_col)


    # Rotate each non-zero pixel and update the output grid.
    for (row, col), value in non_zero_pixels:
      rotated_coords = rotate_point((row, col), center)
      output_grid[rotated_coords] = value


    return output_grid
```
