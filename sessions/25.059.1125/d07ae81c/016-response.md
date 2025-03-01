# d07ae81c • 016 • refine_coder

---
```python
"""
1.  **Identify Azure Seeds:** Locate all pixels colored azure (8) in the input grid.

2.  **Limited Azure Propagation:** For each azure pixel, change any directly adjacent (up, down, left, or right, but *not* diagonally) blue (1) pixels to azure. Other colors block propagation.

3.  **Identify Red Seed:** Find the single pixel colored red (2) in the input grid.

4.  **Limited Red Propagation:**
    *   Red propagates only to the row it starts in and the row directly beneath it.
    *   For an adjacent pixel (including diagonals) of the red pixel, change any blue (1) pixel to red (2). Other colors block propagation.
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
    allowed_rows = [r, r + 1]
    neighbors = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1),
                 (r - 1, c - 1), (r - 1, c + 1), (r + 1, c - 1), (r + 1, c + 1)]
    for nr, nc in neighbors:
        if 0 <= nr < rows and 0 <= nc < cols and nr in allowed_rows and output_grid[nr, nc] == 1:
            output_grid[nr, nc] = 2

    return output_grid
```
