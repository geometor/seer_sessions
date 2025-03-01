# 3ac3eb23 • 004 • example_1 • investigate_coder

---
```python
"""
1.  **Identify Key Pixels:** Locate all red (2) and azure (8) pixels in the input grid.

2.  **Replicate Red Pixels:** For each red pixel:
    *   Create a red pixel directly beneath it.
    *   Create a red pixel diagonally down and to the left.
    * Repeat these two sub-steps until the red color will go out-of-bounds of the grid

3.  **Replicate Azure Pixels:** For each azure pixel:
    *   Create a azure pixel directly beneath it.
    *    Create an azure pixel diagonally down and to the left.
    * Repeat these two sub-steps until the azure color will go out-of-bounds of the grid.

4.  **Output:** Combine all the replicated pixels, along with the original white background, to form the output grid. All the original pixels stay put, replication happens based on their positions.
"""

import numpy as np

def get_pixels_by_color(grid, color):
    """Finds the coordinates of all pixels of a specified color."""
    return np.argwhere(grid == color)

def transform(input_grid):
    """Transforms the input grid according to the replication rule."""
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Replicate red pixels
    for row, col in get_pixels_by_color(input_grid, 2):
        r, c = row, col
        while r + 1 < rows:
            output_grid[r + 1, c] = 2  # Below
            if c - 1 >= 0:
                output_grid[r + 1, c - 1] = 2  # Diagonally down and left
            r += 1
            c -= 1

    # Replicate azure pixels
    for row, col in get_pixels_by_color(input_grid, 8):
        r, c = row, col
        while r + 1 < rows:
            output_grid[r + 1, c] = 8 # Below
            if c - 1 >= 0:
                output_grid[r + 1, c - 1] = 8 # Diagonally down and left
            r += 1
            c -= 1

    return output_grid
```
