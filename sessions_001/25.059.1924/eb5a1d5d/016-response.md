# eb5a1d5d • 016 • example_3 • investigate_coder

---
```python
"""
Locate the single blue (1) pixel in the input grid. Create a 7x7 output grid centered on this pixel.
Reconstruct the nested structure: a blue pixel at the center, surrounded by a 3x3 red square, 
then a 5x5 azure square, and finally a green border filling the rest of the 7x7 grid.
"""

import numpy as np

def find_pixel(grid, color):
    """Finds the coordinates of a pixel of the specified color."""
    coords = np.argwhere(grid == color)
    if len(coords) > 0:
        return coords[0]  # Return the first occurrence
    return None

def transform(input_grid):
    # Find the coordinates of the blue pixel (1).
    blue_pixel_coords = find_pixel(input_grid, 1)

    if blue_pixel_coords is None:
        return None  # Or handle the case where there's no blue pixel

    # Create a 7x7 output grid filled with green (3).
    output_grid = np.full((7, 7), 3)

    # Calculate the center of the output grid.
    center_row, center_col = 3, 3

    # Place the blue pixel at the center.
    output_grid[center_row, center_col] = 1

    # Fill the 3x3 red square around the center.
    for i in range(-1, 2):
        for j in range(-1, 2):
            output_grid[center_row + i, center_col + j] = 2

    # Fill the 5x5 azure square.
    for i in range(-2, 3):
        for j in range(-2, 3):
            output_grid[center_row + i, center_col + j] = 8

    #The above loops fill the pixels in order, so overwrite to correct color values
    # Fill the 3x3 red square around the center.
    for i in range(-1, 2):
        for j in range(-1, 2):
            output_grid[center_row + i, center_col + j] = 2

    # Place the blue pixel at the center.
    output_grid[center_row, center_col] = 1

    return output_grid
```
