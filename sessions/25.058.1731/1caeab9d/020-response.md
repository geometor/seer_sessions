# 1caeab9d • 020 • example_3 • investigate_coder

---
```python
"""
The transformation rule is a conditional downward shift of colored pixels (1, 2, and 4) if the pixel above them is white (0).
"""

import numpy as np

def get_pixels_by_color(grid, colors):
    """
    Finds the coordinates of pixels with specified colors.

    Args:
        grid: The input grid (2D numpy array).
        colors: A list of colors (integers) to search for.

    Returns:
        A list of (row, col) tuples representing the coordinates of the pixels.
    """
    pixels = []
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] in colors:
                pixels.append((r, c))
    return pixels

def transform(input_grid):
    """
    Transforms the input grid by moving colored pixels (1, 2, and 4) down one row
    if the pixel above them is white (0).

    Args:
        input_grid: The input grid (2D numpy array).

    Returns:
        The transformed grid (2D numpy array).
    """
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Identify target pixels (colors 1, 2, and 4)
    target_colors = [1, 2, 4]
    target_pixels = get_pixels_by_color(output_grid, target_colors)


    # Iterate through target pixels and apply the transformation rule
    for r, c in target_pixels:
        # Conditional check: Is the pixel above white (0)?
        if r > 0 and output_grid[r-1, c] == 0:
            # Move Down: Shift the pixel's location one row down.
            output_grid[r, c], output_grid[r - 1, c] =  output_grid[r-1,c], output_grid[r,c]

    return output_grid
```
