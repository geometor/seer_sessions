# 253bf280 • 002 • example_8 • investigate_coder

---
```python
"""
1.  **Identify:** Locate all azure (8) pixels in the input grid.
2. **Analyze Azure Pixel Arrangement**: Determine if there are two or more azure pixels and whether they are arranged either in a straight horizontal or vertical line in the output.
3.  **Conditional Extension:**
    *   If the azure pixels exist in a horizontal or vertical line, fill the space between the azure colored pixels, inclusive of the columns/rows of the edge azure pixels, with green (3) pixels, maintaining the original azure pixel positions. If they cross (both exist in horizontal and vertical, fill both).
    *   If azure pixels are not aligned, or only one azure pixel, keep the output the same as the input.
"""

import numpy as np

def find_pixels_by_color(grid, color):
    """Finds the coordinates of all pixels of a specific color."""
    return np.argwhere(grid == color)

def transform(input_grid):
    """Transforms the input grid based on the azure pixel bridging rule."""
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)
    azure_pixels = find_pixels_by_color(input_grid, 8)

    if len(azure_pixels) > 1:
        # Check for horizontal alignment
        rows = azure_pixels[:, 0]
        if np.all(rows == rows[0]):  # All on the same row
            min_col = np.min(azure_pixels[:, 1])
            max_col = np.max(azure_pixels[:, 1])
            output_grid[rows[0], min_col:max_col+1] = np.where(input_grid[rows[0], min_col:max_col+1] == 8, 8, 3)

        # Check for vertical alignment
        cols = azure_pixels[:, 1]
        if np.all(cols == cols[0]):  # All on the same column
            min_row = np.min(azure_pixels[:, 0])
            max_row = np.max(azure_pixels[:, 0])
            output_grid[min_row:max_row+1, cols[0]] = np.where(input_grid[min_row:max_row+1, cols[0]] == 8, 8, 3)

    return output_grid.tolist()
```
