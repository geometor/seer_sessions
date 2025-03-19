# 6d58a25d • 006 • refine_coder

---
```python
"""
The transformation identifies a maroon (9) shape in the input grid.  It replaces the maroon pixels with azure (8) pixels.
Then, it extends the azure shape downwards. The extension has the same width as the original maroon shape, and its height is
equal to the height of the original maroon shape. Existing azure pixels are preserved.
"""

import numpy as np

def find_shape(grid, color):
    """Finds the coordinates of a contiguous shape of the specified color."""
    coords = np.argwhere(grid == color)
    if coords.size == 0:
        return None, 0, 0
    min_row, min_col = coords.min(axis=0)
    max_row, max_col = coords.max(axis=0)
    height = max_row - min_row + 1
    width = max_col - min_col + 1
    return (min_row, min_col), height, width

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid.
    output_grid = np.copy(input_grid)

    # Find existing azure pixels
    azure_pixels = np.argwhere(input_grid == 8)

    # Find the maroon shape and its dimensions.
    maroon_coords, maroon_height, maroon_width = find_shape(input_grid, 9)

    if maroon_coords:
        min_row, min_col = maroon_coords

        # Replace maroon pixels with azure.
        for r in range(maroon_height):
            for c in range(maroon_width):
                output_grid[min_row + r, min_col + c] = 8

        # Extend the azure shape downwards.
        for r in range(maroon_height):
           for c in range(maroon_width):
                output_grid[min_row + maroon_height + r, min_col + c] = 8
    
    # Preserve existing azure pixels.
    for row, col in azure_pixels:
        output_grid[row, col] = 8

    return output_grid
```
