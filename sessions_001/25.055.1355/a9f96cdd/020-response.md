# a9f96cdd • 020 • example_4 • investigate_coder

---
```python
"""
Places four colored pixels (green, magenta, azure, orange) around a central point defined by the location of a red pixel in the input grid. The positions of the new pixels are diagonally adjacent to the red pixel's location.
"""

import numpy as np

def find_red_pixel(grid):
    # Find the coordinates of the red pixel (value 2).
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == 2:
                return (r, c)
    return None  # Should not happen in a valid input, but added for safety

def transform(input_grid):
    # Initialize output_grid with the same dimensions and filled with white (0).
    output_grid = np.zeros_like(input_grid)

    # Find the red pixel's location.
    red_pixel_coords = find_red_pixel(input_grid)

    if red_pixel_coords is None:
        return output_grid # handles edge case but should not occur

    r, c = red_pixel_coords

    # Create the four colored pixels based on the red pixel's position.
    if r > 0 and c > 0:
        output_grid[r - 1, c - 1] = 3  # Green
    if r > 0 and c < output_grid.shape[1] - 1:
        output_grid[r - 1, c + 1] = 6  # Magenta
    if r < output_grid.shape[0] - 1 and c > 0:
        output_grid[r + 1, c - 1] = 8  # Azure
    if r < output_grid.shape[0] - 1 and c < output_grid.shape[1] - 1:
        output_grid[r + 1, c + 1] = 7  # Orange

    return output_grid
```
