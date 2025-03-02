# 253bf280 • 044 • refine_coder

---
```python
"""
1.  **Find Azure Pixels:** Locate all azure (8) colored pixels in the input grid.
2.  **Bounding Box:** Determine the bounding box of the azure pixels. This is defined by the minimum and maximum row and column indices of all azure pixels.
3.  **Green Line Column:** The green line will be drawn in the left-most column occupied by azure pixels (bounding_box.min_col).
4.  **Green Line Start Row:** The green line starts one row *above* the top-most azure pixel.  Calculate this as `max(0, bounding_box.min_row - 1)`. This ensures the line starts at the top of the grid if the calculated value is negative.
5.  **Green Line End Row:** The green line ends one row *above* the bottom-most azure pixel. Calculate this as 'max(0, bounding_box.max_row - 1)`.
6.  **Draw Green Line:** Draw a vertical line of green (3) pixels in the output grid, using the calculated start row, end row, and column.
7. **No Azure Pixels:** If there are no azure pixels, return the input grid unchanged.
"""

import numpy as np

def get_azure_pixels(grid):
    """Finds coordinates of azure (8) pixels."""
    azure_coords = np.where(grid == 8)
    return list(zip(azure_coords[0], azure_coords[1]))

def get_bounding_box(pixels):
    """Calculates the bounding box of a list of pixels."""
    if not pixels:
        return None
    min_row, min_col = np.min(pixels, axis=0)
    max_row, max_col = np.max(pixels, axis=0)
    return {"min_row": min_row, "max_row": max_row, "min_col": min_col, "max_col": max_col}

def transform(input_grid):
    """Transforms the input grid by drawing a vertical green line based on azure pixel bounding box."""

    # Initialize the output grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    grid_height = output_grid.shape[0]

    # Find the azure pixels
    azure_pixels = get_azure_pixels(input_grid)

    # If no azure pixels are found, return a copy of the input
    if not azure_pixels:
        return output_grid

    # Determine bounding box
    bounding_box = get_bounding_box(azure_pixels)

    # Determine green line column
    green_column = bounding_box["min_col"]

    # Determine green line start row
    green_start_row = max(0, bounding_box["min_row"] - 1)

    # Determine green line end row
    green_end_row = max(0, bounding_box["max_row"] - 1)


    # Draw the green line (3)
    for row in range(green_start_row, green_end_row + 1):
        if 0 <= row < grid_height:
            output_grid[row, green_column] = 3

    return output_grid
```
