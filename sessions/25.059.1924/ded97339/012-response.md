# ded97339 • 012 • refine_coder

---
```python
"""
1.  **Locate Azure Pixels:** Identify the (x, y) coordinates of all azure (8) pixels in the input grid.
2.  **Draw Vertical Lines:** For each azure pixel, draw a vertical line of azure pixels across the entire height of the grid. The x-coordinate of the vertical line is the same as the x-coordinate of the original azure pixel.
3.  **Draw Horizontal Lines:** For each azure pixel, draw a horizontal line of azure pixels across the entire width of the grid. The y-coordinate of the horizontal line is the same as the y-coordinate of the original azure pixel.
4. The output is a grid containing all the vertical lines and the horizontal lines.
"""

import numpy as np

def find_azure_pixels(grid):
    # Find coordinates of all azure (8) pixels
    return np.argwhere(grid == 8)

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""
    output_grid = np.copy(input_grid)
    azure_pixels = find_azure_pixels(input_grid)

    # Vertical Propagation
    for x, y in azure_pixels:
        for i in range(output_grid.shape[0]):
            output_grid[i, x] = 8

    # Horizontal Propagation
    for x, y in azure_pixels:
        for j in range(output_grid.shape[1]):
            output_grid[y, j] = 8

    return output_grid
```

