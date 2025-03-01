# a1570a43 • 026 • refine_coder

---
```python
"""
1.  Identify Red Pixels: Locate all red pixels (value 2) in the input grid.
2.  Check Adjacency: For each red pixel, examine its immediate neighbors (left, right, and above).
3.  Extend Red:
    *   If a red pixel has a white pixel (value 0) immediately to its left, add a red pixel to the left of the current red pixel in the output grid.
    *   If a red pixel has a white pixel (value 0) immediately to its right, add a red pixel to the right of the current red pixel in the output grid.
    *   If a red pixel has a white pixel (value 0) immediately above it, add a red pixel above the current red pixel in the output grid.
4.  If a red pixel has another red pixel (value 2) above, below, left, and
    right, do nothing.
5.  Preserve Originals: The original red pixels should remain in their original positions. The transformation *adds* red pixels based on adjacency; it does not *move* them.
"""

import numpy as np

def get_adjacent_colors(grid, row, col):
    """Returns a set of colors adjacent to the given cell (up, down, left, right)."""
    adjacent_colors = set()
    rows, cols = grid.shape
    for dr, dc in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # Only check left, right, up, down
        r, c = row + dr, col + dc
        if 0 <= r < rows and 0 <= c < cols:
            adjacent_colors.add(grid[r, c])
    return adjacent_colors

def transform(input_grid):
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid)
    input_grid = np.array(input_grid)  # make sure we're working with a numpy array
    
    # Find red pixels
    red_pixels = np.where(input_grid == 2)
    red_pixel_coordinates = list(zip(red_pixels[0], red_pixels[1]))

    # Iterate through red pixels
    for row, col in red_pixel_coordinates:
        # Check left
        if col > 0 and input_grid[row, col - 1] == 0:
            output_grid[row, col - 1] = 2
        # Check right
        if col < input_grid.shape[1] - 1 and input_grid[row, col + 1] == 0:
            output_grid[row, col + 1] = 2
        # Check up
        if row > 0 and input_grid[row - 1, col] == 0:
            output_grid[row - 1, col] = 2

    return output_grid
```
