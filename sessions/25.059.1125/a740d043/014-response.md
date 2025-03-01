# a740d043 • 014 • refine_coder

---
```python
"""
1.  **Identify Single Pixels:** Locate all single pixels (those not adjacent to a pixel of the same color) of color other than blue (color 1).
2.  **Extract Colors:** Get the colors of those identified single pixels.
3.  **Add White:** Include white (color 0) in the set of colors.
4. **Arrange Horizontally:** Create a new grid where these colors (Green, White, and Red) are arranged as a single horizontal row, maintaining that specific order.
5.  **Duplicate Row:** Duplicate this row to create a second identical row below the first.
6. **Output:** The new grid should have the dimensions 2 x 3, with the colors in the specified order and duplicated vertically.
"""

import numpy as np

def is_single_pixel(grid, row, col):
    """Checks if a pixel is a single pixel (not adjacent to the same color)."""
    color = grid[row, col]
    height, width = grid.shape

    # Check adjacent pixels (up, down, left, right)
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < height and 0 <= new_col < width and grid[new_row, new_col] == color:
            return False  # Found an adjacent pixel of the same color
    return True

def transform(input_grid):
    """Transforms the input grid according to the rules."""
    height, width = input_grid.shape
    single_pixel_colors = []

    # Find single pixels of colors other than blue (1)
    for r in range(height):
        for c in range(width):
            if input_grid[r, c] != 1 and is_single_pixel(input_grid, r, c):
                single_pixel_colors.append(input_grid[r, c])

    # Create the output grid
    output_colors = []

    # Check for green (3), red(2) in single pixel and insert to output_colors with white(0)
    if 3 in single_pixel_colors:
        output_colors.append(3)
    if 0 not in output_colors:
       output_colors.append(0)
    if 2 in single_pixel_colors:
        output_colors.append(2)
    
    output_grid = np.array([output_colors, output_colors])

    return output_grid
```
