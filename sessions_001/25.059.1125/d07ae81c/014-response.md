# d07ae81c • 014 • refine_coder

---
```python
"""
1.  **Identify Azure Seeds:** Find all pixels with color 8 (azure) in the input grid.
2.  **Limited Azure Propagation:** For each azure pixel, change any directly adjacent (non-diagonal) blue (color 1) pixels to azure.
3.  **Identify Red Seed:** Find the single pixel with color 2 (red) in the input grid.
4.  **Limited Red Propagation:** Find all blue pixels (color 1) that are directly adjacent (including diagonals) to the red pixel. Change these blue pixels to red.
"""

import numpy as np

def get_pixels_by_color(grid, color):
    """Finds the coordinates of all pixels of a specific color."""
    return np.argwhere(grid == color)

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    # Find azure seed pixels
    azure_pixels = get_pixels_by_color(input_grid, 8)

    # Limited Azure Propagation
    for row, col in azure_pixels:
        neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
        for r, c in neighbors:
            if 0 <= r < rows and 0 <= c < cols and output_grid[r, c] == 1:
                output_grid[r, c] = 8

    # Find red seed pixel
    red_pixels = get_pixels_by_color(input_grid, 2)
    if len(red_pixels) > 0:
      single_red_pixel = red_pixels[0]  # Assuming there's only one
    else:
       return output_grid # safeguard

    # Limited Red Propagation
    r, c = single_red_pixel
    neighbors = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1),
                 (r - 1, c - 1), (r - 1, c + 1), (r + 1, c - 1), (r + 1, c + 1)]
    for nr, nc in neighbors:
        if 0 <= nr < rows and 0 <= nc < cols and output_grid[nr, nc] == 1:
            output_grid[nr, nc] = 2

    return output_grid
```
