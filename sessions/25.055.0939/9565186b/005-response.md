# 9565186b • 005 • refine_coder

---
```python
"""
Identify all blue (1) pixels in the input grid.
Identify the single azure (8) pixel in the input grid.
Transform all blue pixels to black (0) pixels.
Maintain the azure pixel at its original location and color.
"""

import numpy as np

def find_pixel(grid, color):
    """Finds the coordinates of a specific color pixel in the grid."""
    # np.where returns a tuple of arrays, one for each dimension.
    coords = np.where(grid == color)
    # Check if exactly one pixel of the specified color was found.
    if len(coords[0]) == 1 and len(coords[1]) == 1:
        return coords[0][0], coords[1][0]  # Return row and column
    else:
        return None  # Or handle the case where there are 0 or >1 pixels.


def transform(input_grid):
    """Transforms the input grid according to the rule."""
    # Initialize the output grid as a copy of the input grid.
    output_grid = input_grid.copy()

    # Find the azure pixel (expecting only one)
    azure_coords = find_pixel(input_grid, 8)

    # Replace all blue pixels with black pixels
    output_grid[output_grid == 1] = 0

    # Ensure azure pixel is preserved (already in correct position)
    if azure_coords: # verify it was found
       # output_grid[azure_coords] = 8  # Redundant as the copy took care.

        pass
    return output_grid
```

